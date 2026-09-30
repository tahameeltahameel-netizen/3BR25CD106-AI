/**
 * app.js - Dashboard Logic and Visualizations for T20 Cricket Analytics
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Load Match Data
  const rawMatches = window.getMatches ? window.getMatches() : [];

  // DOM Elements
  const seasonSelect = document.getElementById('filter-season');
  const teamSelect = document.getElementById('filter-team');
  const venueSelect = document.getElementById('filter-venue');
  const resetBtn = document.getElementById('reset-filters-btn');

  const kpiMatchesPlayed = document.getElementById('kpi-matches-played');
  const kpiAvgFirstInnings = document.getElementById('kpi-avg-first-innings');
  const kpiAvgPowerplay = document.getElementById('kpi-avg-powerplay');
  const kpiTossWinPct = document.getElementById('kpi-toss-win-pct');
  const kpiBatFirstWinPct = document.getElementById('kpi-bat-first-win-pct');

  const insightsTextContainer = document.getElementById('insights-text');

  // Chart Instances Registry
  let chartPowerplaySeason = null;
  let chartFirstInningsSeason = null;
  let chartTeamWinRate = null;
  let chartVenueBatVsChase = null;

  // Extract Master Dimensions
  const allSeasons = [...new Set(rawMatches.map((m) => m.y))].sort((a, b) => a - b);
  const allTeams = [...new Set(rawMatches.flatMap((m) => [m.a, m.b]))].sort();
  const allVenues = [...new Set(rawMatches.map((m) => m.v))].sort();

  // Populate Filter Dropdowns
  populateDropdown(seasonSelect, allSeasons);
  populateDropdown(teamSelect, allTeams);
  populateDropdown(venueSelect, allVenues);

  function populateDropdown(selectElement, items) {
    items.forEach((item) => {
      const option = document.createElement('option');
      option.value = item;
      option.textContent = item;
      selectElement.appendChild(option);
    });
  }

  // Helper for CSS Variable theme extraction
  function getThemeColors() {
    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    return {
      text: isDark ? '#cbd5e1' : '#475569',
      grid: isDark ? '#334155' : '#e2e8f0',
      primary: isDark ? '#60a5fa' : '#2563eb',
      primaryAlpha: isDark ? 'rgba(96, 165, 250, 0.25)' : 'rgba(37, 99, 235, 0.2)',
      secondary: isDark ? '#34d399' : '#10b981',
      secondaryAlpha: isDark ? 'rgba(52, 211, 153, 0.25)' : 'rgba(16, 185, 129, 0.2)',
      accent: isDark ? '#fbbf24' : '#f59e0b',
      accentAlpha: isDark ? 'rgba(251, 191, 36, 0.25)' : 'rgba(245, 158, 11, 0.2)'
    };
  }

  // Filter Matching Function
  function getFilteredMatches() {
    const selectedSeason = seasonSelect.value;
    const selectedTeam = teamSelect.value;
    const selectedVenue = venueSelect.value;

    return rawMatches.filter((m) => {
      const seasonMatch = selectedSeason === 'All' || String(m.y) === selectedSeason;
      const teamMatch = selectedTeam === 'All' || m.a === selectedTeam || m.b === selectedTeam;
      const venueMatch = selectedVenue === 'All' || m.v === selectedVenue;
      return seasonMatch && teamMatch && venueMatch;
    });
  }

  // Update KPIs
  function updateKPIs(matches) {
    const total = matches.length;
    if (total === 0) {
      kpiMatchesPlayed.textContent = '0';
      kpiAvgFirstInnings.textContent = '-';
      kpiAvgPowerplay.textContent = '-';
      kpiTossWinPct.textContent = '-';
      kpiBatFirstWinPct.textContent = '-';
      return;
    }

    const sumFirst = matches.reduce((acc, m) => acc + m.first, 0);
    const sumPP = matches.reduce((acc, m) => acc + m.pp, 0);
    const tossWins = matches.filter((m) => m.tossWin === m.w).length;
    const batFirstWins = matches.filter((m) => m.bf === m.w).length;

    kpiMatchesPlayed.textContent = total;
    kpiAvgFirstInnings.textContent = (sumFirst / total).toFixed(1);
    kpiAvgPowerplay.textContent = (sumPP / total).toFixed(1);
    kpiTossWinPct.textContent = ((tossWins / total) * 100).toFixed(1) + '%';
    kpiBatFirstWinPct.textContent = ((batFirstWins / total) * 100).toFixed(1) + '%';
  }

  // Generate Insights Text (4-5 dynamic sentences)
  function updateInsights(matches) {
    if (matches.length === 0) {
      insightsTextContainer.textContent = 'No match data available for the selected filters. Please adjust your criteria.';
      return;
    }

    const total = matches.length;
    const tossWins = matches.filter((m) => m.tossWin === m.w).length;
    const tossWinPct = ((tossWins / total) * 100).toFixed(1);

    const batFirstWins = matches.filter((m) => m.bf === m.w).length;
    const batFirstWinPct = ((batFirstWins / total) * 100).toFixed(1);
    const chasingWinPct = (100 - parseFloat(batFirstWinPct)).toFixed(1);

    // Sentence 1: Toss Impact
    const sentence1 = `Across the ${total} selected match${total === 1 ? '' : 'es'}, winning the toss proved decisive in ${tossWinPct}% of fixtures.`;

    // Sentence 2: Field-first vs Bat-first Decision Advantage
    const preference = parseFloat(batFirstWinPct) >= 50 ? 'defending targets' : 'chasing targets';
    const sentence2 = `Teams batting first secured victory ${batFirstWinPct}% of the time, highlighting a slight statistical edge for ${preference}.`;

    // Sentence 3: Best Venue for Batting First
    let bestVenueName = 'N/A';
    let bestVenueBatFirstPct = -1;
    allVenues.forEach((v) => {
      const vMatches = matches.filter((m) => m.v === v);
      if (vMatches.length > 0) {
        const vBatFirstWins = vMatches.filter((m) => m.bf === m.w).length;
        const pct = (vBatFirstWins / vMatches.length) * 100;
        if (pct > bestVenueBatFirstPct) {
          bestVenueBatFirstPct = pct;
          bestVenueName = v;
        }
      }
    });
    const sentence3 = bestVenueBatFirstPct >= 0
      ? `${bestVenueName} emerged as the most favorable venue for teams batting first, yielding a ${bestVenueBatFirstPct.toFixed(1)}% win rate for defenders.`
      : `Venue performance was evenly balanced across the selected criteria.`;

    // Sentence 4: Powerplay Change Across Seasons
    const seasonsInSet = [...new Set(matches.map((m) => m.y))].sort((a, b) => a - b);
    let sentence4 = '';
    if (seasonsInSet.length > 1) {
      const firstSeason = seasonsInSet[0];
      const lastSeason = seasonsInSet[seasonsInSet.length - 1];
      const firstSeasonMatches = matches.filter((m) => m.y === firstSeason);
      const lastSeasonMatches = matches.filter((m) => m.y === lastSeason);
      const avgPPFirst = (firstSeasonMatches.reduce((acc, m) => acc + m.pp, 0) / firstSeasonMatches.length).toFixed(1);
      const avgPPLast = (lastSeasonMatches.reduce((acc, m) => acc + m.pp, 0) / lastSeasonMatches.length).toFixed(1);
      const diff = (parseFloat(avgPPLast) - parseFloat(avgPPFirst)).toFixed(1);
      const direction = diff >= 0 ? 'increased' : 'decreased';
      sentence4 = `Powerplay scoring ${direction} from an average of ${avgPPFirst} runs in ${firstSeason} to ${avgPPLast} runs in ${lastSeason}.`;
    } else if (seasonsInSet.length === 1) {
      const seasonPP = (matches.reduce((acc, m) => acc + m.pp, 0) / total).toFixed(1);
      sentence4 = `In Season ${seasonsInSet[0]}, teams averaged a powerplay score of ${seasonPP} runs in the opening six overs.`;
    } else {
      sentence4 = `Powerplay scores remained consistent throughout the analyzed timeframe.`;
    }

    // Sentence 5: Top Team
    let topTeamName = 'N/A';
    let topTeamWinRate = -1;
    allTeams.forEach((t) => {
      const tMatches = matches.filter((m) => m.a === t || m.b === t);
      if (tMatches.length > 0) {
        const tWins = matches.filter((m) => m.w === t).length;
        const winRate = (tWins / tMatches.length) * 100;
        if (winRate > topTeamWinRate) {
          topTeamWinRate = winRate;
          topTeamName = t;
        }
      }
    });
    const sentence5 = topTeamWinRate >= 0
      ? `${topTeamName} stood out as the top performer in this dataset with an impressive ${topTeamWinRate.toFixed(1)}% win rate.`
      : `Team performances were highly competitive across all fixtures.`;

    insightsTextContainer.textContent = `${sentence1} ${sentence2} ${sentence3} ${sentence4} ${sentence5}`;
  }

  // Render Charts
  function renderCharts(matches) {
    const colors = getThemeColors();

    // Common Chart Options
    const commonOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            color: colors.text,
            font: { family: 'inherit', size: 12 }
          }
        },
        tooltip: {
          padding: 10,
          cornerRadius: 6
        }
      },
      scales: {
        x: {
          ticks: { color: colors.text },
          grid: { color: colors.grid }
        },
        y: {
          ticks: { color: colors.text },
          grid: { color: colors.grid }
        }
      }
    };

    // 1. Powerplay Score by Season (Line)
    const seasonLabels = allSeasons.map(String);
    const ppData = allSeasons.map((s) => {
      const seasonMatches = matches.filter((m) => m.y === s);
      if (seasonMatches.length === 0) return null;
      return (seasonMatches.reduce((acc, m) => acc + m.pp, 0) / seasonMatches.length).toFixed(1);
    });

    if (chartPowerplaySeason) chartPowerplaySeason.destroy();
    const ctxPP = document.getElementById('chart-powerplay-season').getContext('2d');
    chartPowerplaySeason = new Chart(ctxPP, {
      type: 'line',
      data: {
        labels: seasonLabels,
        datasets: [{
          label: 'Avg Powerplay Score',
          data: ppData,
          borderColor: colors.primary,
          backgroundColor: colors.primaryAlpha,
          borderWidth: 2,
          fill: true,
          tension: 0.3,
          pointRadius: 4,
          pointHoverRadius: 6
        }]
      },
      options: {
        ...commonOptions,
        scales: {
          ...commonOptions.scales,
          y: { ...commonOptions.scales.y, title: { display: true, text: 'Runs', color: colors.text } }
        }
      }
    });

    // 2. First-Innings Score by Season (Line)
    const firstInningsData = allSeasons.map((s) => {
      const seasonMatches = matches.filter((m) => m.y === s);
      if (seasonMatches.length === 0) return null;
      return (seasonMatches.reduce((acc, m) => acc + m.first, 0) / seasonMatches.length).toFixed(1);
    });

    if (chartFirstInningsSeason) chartFirstInningsSeason.destroy();
    const ctxFirst = document.getElementById('chart-first-innings-season').getContext('2d');
    chartFirstInningsSeason = new Chart(ctxFirst, {
      type: 'line',
      data: {
        labels: seasonLabels,
        datasets: [{
          label: 'Avg 1st-Innings Score',
          data: firstInningsData,
          borderColor: colors.secondary,
          backgroundColor: colors.secondaryAlpha,
          borderWidth: 2,
          fill: true,
          tension: 0.3,
          pointRadius: 4,
          pointHoverRadius: 6
        }]
      },
      options: {
        ...commonOptions,
        scales: {
          ...commonOptions.scales,
          y: { ...commonOptions.scales.y, title: { display: true, text: 'Runs', color: colors.text } }
        }
      }
    });

    // 3. Win % by Team (Horizontal Bar)
    const activeTeams = teamSelect.value !== 'All'
      ? [teamSelect.value]
      : allTeams;

    const teamWinData = activeTeams.map((team) => {
      const tMatches = matches.filter((m) => m.a === team || m.b === team);
      if (tMatches.length === 0) return { team, winPct: 0 };
      const wins = matches.filter((m) => m.w === team).length;
      return { team, winPct: parseFloat(((wins / tMatches.length) * 100).toFixed(1)) };
    }).sort((a, b) => b.winPct - a.winPct);

    if (chartTeamWinRate) chartTeamWinRate.destroy();
    const ctxTeam = document.getElementById('chart-team-win-rate').getContext('2d');
    chartTeamWinRate = new Chart(ctxTeam, {
      type: 'bar',
      data: {
        labels: teamWinData.map((d) => d.team),
        datasets: [{
          label: 'Win %',
          data: teamWinData.map((d) => d.winPct),
          backgroundColor: colors.primary,
          borderRadius: 4
        }]
      },
      options: {
        ...commonOptions,
        indexAxis: 'y',
        scales: {
          x: { ...commonOptions.scales.x, max: 100, title: { display: true, text: 'Win %', color: colors.text } },
          y: { ...commonOptions.scales.y }
        }
      }
    });

    // 4. Batting First vs Chasing Win % by Venue (Grouped Bar)
    const activeVenues = venueSelect.value !== 'All'
      ? [venueSelect.value]
      : allVenues;

    const batFirstVenuePcts = [];
    const chaseVenuePcts = [];

    activeVenues.forEach((venue) => {
      const vMatches = matches.filter((m) => m.v === venue);
      if (vMatches.length === 0) {
        batFirstVenuePcts.push(0);
        chaseVenuePcts.push(0);
      } else {
        const batFirstWins = vMatches.filter((m) => m.bf === m.w).length;
        const chaseWins = vMatches.filter((m) => m.ch === m.w).length;
        batFirstVenuePcts.push(parseFloat(((batFirstWins / vMatches.length) * 100).toFixed(1)));
        chaseVenuePcts.push(parseFloat(((chaseWins / vMatches.length) * 100).toFixed(1)));
      }
    });

    if (chartVenueBatVsChase) chartVenueBatVsChase.destroy();
    const ctxVenue = document.getElementById('chart-venue-bat-vs-chase').getContext('2d');
    chartVenueBatVsChase = new Chart(ctxVenue, {
      type: 'bar',
      data: {
        labels: activeVenues,
        datasets: [
          {
            label: 'Batting First Win %',
            data: batFirstVenuePcts,
            backgroundColor: colors.primary,
            borderRadius: 4
          },
          {
            label: 'Chasing Win %',
            data: chaseVenuePcts,
            backgroundColor: colors.accent,
            borderRadius: 4
          }
        ]
      },
      options: {
        ...commonOptions,
        scales: {
          ...commonOptions.scales,
          y: { ...commonOptions.scales.y, max: 100, title: { display: true, text: 'Win %', color: colors.text } }
        }
      }
    });
  }

  // Master Render & Update Controller
  function updateDashboard() {
    const filteredMatches = getFilteredMatches();
    updateKPIs(filteredMatches);
    updateInsights(filteredMatches);
    renderCharts(filteredMatches);
  }

  // Event Listeners
  seasonSelect.addEventListener('change', updateDashboard);
  teamSelect.addEventListener('change', updateDashboard);
  venueSelect.addEventListener('change', updateDashboard);

  resetBtn.addEventListener('click', () => {
    seasonSelect.value = 'All';
    teamSelect.value = 'All';
    venueSelect.value = 'All';
    updateDashboard();
  });

  // Watch for system theme change to update chart styling dynamically
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    updateDashboard();
  });

  // Initial render
  updateDashboard();
});
