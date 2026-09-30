/**
 * data.js - Synthetic Data Generator for T20 Cricket Analytics Dashboard
 *
 * Provides deterministic synthetic match data across 7 seasons (2018-2024).
 * Matches schema: { y, a, b, v, tossWin, bf, ch, w, first, second, pp }
 */

(function () {
  // Simple Mulberry32 Seeded Random Number Generator
  function mulberry32(seed) {
    return function () {
      let t = (seed += 0x6d2b79f5);
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  const SEASONS = [2018, 2019, 2020, 2021, 2022, 2023, 2024];
  const TEAMS = [
    'Mumbai Dynamites',
    'Chennai Super Giants',
    'Bangalore Royals',
    'Kolkata Knight Warriors',
    'Delhi Panthers',
    'Punjab Kings',
    'Rajasthan Titans',
    'Hyderabad Chargers'
  ];
  const VENUES = [
    'Wankhede Stadium',
    'M. A. Chidambaram Stadium',
    'M. Chinnaswamy Stadium',
    'Eden Gardens',
    'Narendra Modi Stadium'
  ];

  function generateSyntheticMatches() {
    const random = mulberry32(42);
    const matches = [];

    SEASONS.forEach((year) => {
      // ~56 matches per season (round robin style)
      for (let i = 0; i < TEAMS.length; i++) {
        for (let j = i + 1; j < TEAMS.length; j++) {
          // Play 2 matches per team pair (home/away or 2 encounters per season)
          for (let encounter = 0; encounter < 2; encounter++) {
            const teamA = TEAMS[i];
            const teamB = TEAMS[j];
            const venue = VENUES[Math.floor(random() * VENUES.length)];

            // Toss decision
            const tossWin = random() < 0.5 ? teamA : teamB;
            // 55% chance toss winner elects to field (chase)
            const tossWinnerElectedToBat = random() < 0.45;
            const bf = tossWinnerElectedToBat ? tossWin : (tossWin === teamA ? teamB : teamA);
            const ch = bf === teamA ? teamB : teamA;

            // Powerplay score: between 38 and 68 with slight trend over seasons
            const yearBonus = (year - 2018) * 0.8;
            const pp = Math.floor(38 + yearBonus + random() * 26);

            // First innings total score: T20 typical 135 to 215
            const first = Math.floor(135 + yearBonus * 1.5 + random() * 75);

            // Outcome determination
            // 52% chasing win rate bias in T20s
            const chasingWins = random() < 0.52;
            let second, winner;

            if (chasingWins) {
              winner = ch;
              // Target reached (first + 1 to first + 6)
              second = first + 1 + Math.floor(random() * 5);
            } else {
              winner = bf;
              // Defended successfully: second innings score is less
              const margin = 1 + Math.floor(random() * 35);
              second = Math.max(80, first - margin);
            }

            matches.push({
              y: year,
              a: teamA,
              b: teamB,
              v: venue,
              tossWin: tossWin,
              bf: bf,
              ch: ch,
              w: winner,
              first: first,
              second: second,
              pp: pp
            });
          }
        }
      }
    });

    return matches;
  }

  const cachedMatches = generateSyntheticMatches();

  /**
   * Returns the dataset of T20 matches.
   * Can be replaced with real API / data fetching later without changing other UI modules.
   * @returns {Array<Object>} List of match objects.
   */
  window.getMatches = function getMatches() {
    return cachedMatches;
  };
})();
