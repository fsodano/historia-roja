import type { Match, MatchStats, TeamStats } from './types';

const CSV_FILES = [
  '/data/1912.csv', '/data/1913.csv', '/data/1914.csv', '/data/1915.csv', '/data/1916.csv',
  '/data/1917.csv', '/data/1918.csv', '/data/1919.csv', '/data/1920.csv', '/data/1921.csv',
  '/data/1922.csv', '/data/1923.csv', '/data/1924.csv', '/data/1925.csv', '/data/1926.csv',
  '/data/1927.csv', '/data/1928.csv', '/data/1929.csv', '/data/1930.csv', '/data/1931.csv',
  '/data/1932.csv', '/data/1933.csv', '/data/1934.csv', '/data/1935.csv', '/data/1936.csv',
  '/data/1937.csv', '/data/1938.csv', '/data/1939.csv', '/data/1940.csv', '/data/1941.csv',
  '/data/1942.csv', '/data/1943.csv', '/data/1944.csv', '/data/1945.csv', '/data/1946.csv',
  '/data/1947.csv', '/data/1948.csv', '/data/1949.csv', '/data/1950.csv', '/data/1951.csv',
  '/data/1952.csv', '/data/1953.csv', '/data/1954.csv', '/data/1955.csv', '/data/1956.csv',
  '/data/1957.csv', '/data/1958.csv', '/data/1959.csv', '/data/1960.csv', '/data/1961.csv',
  '/data/1962.csv', '/data/1963.csv', '/data/1964.csv', '/data/1965.csv', '/data/1966.csv',
  '/data/1967.csv', '/data/1968.csv', '/data/1969.csv', '/data/1970.csv', '/data/1971.csv',
  '/data/1972.csv', '/data/1973.csv', '/data/1974.csv', '/data/1975.csv', '/data/1976.csv',
  '/data/1977.csv', '/data/1978.csv', '/data/1979.csv', '/data/1980.csv', '/data/1981.csv',
  '/data/1982.csv', '/data/1983.csv', '/data/1984.csv', '/data/1985.csv', '/data/2010.csv',
  '/data/2011.csv', '/data/2012.csv', '/data/2013.csv', '/data/2015.csv', '/data/2016.csv',
  '/data/2017.csv', '/data/2019.csv', '/data/2020.csv', '/data/2021.csv', '/data/2022.csv',
  '/data/2023.csv', '/data/2024.csv', '/data/2025.csv', '/data/2026.csv'
];

let cachedMatches: Match[] | null = null;

export async function loadMatches(): Promise<Match[]> {
  if (cachedMatches) return cachedMatches;
  
  const matches: Match[] = [];
  let matchId = 0;
  
  const fetchPromises = CSV_FILES.map(async (file) => {
    try {
      const response = await fetch(file);
      if (!response.ok) return;
      const content = await response.text();
      const lines = content.trim().split('\n');
      
      for (let i = 1; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!line) continue;
        
        const parts = parseCSVLine(line);
        if (parts.length < 6) continue;
        
        const [date, competition, homeTeam, awayTeam, homeScoreStr, awayScoreStr] = parts;
        const homeGoals = parseInt(homeScoreStr);
        const awayGoals = parseInt(awayScoreStr);
        
        if (isNaN(homeGoals) || isNaN(awayGoals)) continue;
        
        const isIndependienteHome = homeTeam === 'Independiente';
        const isIndependienteAway = awayTeam === 'Independiente';
        
        if (!isIndependienteHome && !isIndependienteAway) continue;
        
        const opponent = isIndependienteHome ? awayTeam : homeTeam;
        
        let independienteGoals = isIndependienteHome ? homeGoals : awayGoals;
        let opponentGoals = isIndependienteHome ? awayGoals : homeGoals;
        
        let resultCode: 'W' | 'L' | 'D';
        if (independienteGoals > opponentGoals) resultCode = 'W';
        else if (independienteGoals < opponentGoals) resultCode = 'L';
        else resultCode = 'D';
        
        matches.push({
          id: `match-${matchId++}`,
          date,
          competition: competition || 'Primera División',
          homeTeam,
          awayTeam,
          homeGoals,
          awayGoals,
          isHome: isIndependienteHome,
          result: resultCode,
          opponent,
          year: extractYear(date)
        });
      }
    } catch {
    }
  });
  
  await Promise.all(fetchPromises);
  
  cachedMatches = matches.sort((a, b) => {
    const dateA = parseDate(a.date);
    const dateB = parseDate(b.date);
    return dateB.getTime() - dateA.getTime();
  });
  
  return cachedMatches;
}

export function parseMatches(): Match[] {
  if (cachedMatches) return cachedMatches;
  return [];
}

function parseCSVLine(line: string): string[] {
  const result: string[] = [];
  let current = '';
  let inQuotes = false;
  
  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    const nextChar = line[i + 1];
    
    if (char === '"') {
      if (inQuotes && nextChar === '"') {
        current += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (char === ',' && !inQuotes) {
      result.push(current.trim());
      current = '';
    } else {
      current += char;
    }
  }
  
  result.push(current.trim());
  return result;
}

function extractYear(dateStr: string): number | null {
  if (!dateStr) return null;
  const yearMatch = dateStr.match(/\b(19|20)\d{2}\b/);
  if (yearMatch) {
    return parseInt(yearMatch[0]);
  }
  return null;
}

function parseDate(dateStr: string): Date {
  if (!dateStr) return new Date(0);
  
  const parts = dateStr.split('/');
  if (parts.length === 3) {
    const day = parseInt(parts[0]);
    const month = parseInt(parts[1]) - 1;
    const year = parseInt(parts[2]);
    if (!isNaN(day) && !isNaN(month) && !isNaN(year)) {
      return new Date(year, month, day);
    }
  }
  
  const parsed = new Date(dateStr);
  return isNaN(parsed.getTime()) ? new Date(0) : parsed;
}

export function calculateStats(matches: Match[]): MatchStats {
  const wins = matches.filter(m => m.result === 'W').length;
  const losses = matches.filter(m => m.result === 'L').length;
  const draws = matches.filter(m => m.result === 'D').length;

  let goalsScored = 0;
  let goalsConceded = 0;

  for (const match of matches) {
    if (match.isHome) {
      goalsScored += match.homeGoals;
      goalsConceded += match.awayGoals;
    } else {
      goalsScored += match.awayGoals;
      goalsConceded += match.homeGoals;
    }
  }

  return {
    totalMatches: matches.length,
    wins,
    losses,
    draws,
    goalsScored,
    goalsConceded,
    goalDifference: goalsScored - goalsConceded,
    winPercentage: matches.length > 0 ? (wins / matches.length) * 100 : 0
  };
}

export function calculateTeamStats(matches: Match[]): TeamStats[] {
  const teamMap = new Map<string, TeamStats>();

  for (const match of matches) {
    const opponent = match.opponent;
    
    if (!teamMap.has(opponent)) {
      teamMap.set(opponent, {
        team: opponent,
        played: 0,
        wins: 0,
        losses: 0,
        draws: 0,
        goalsFor: 0,
        goalsAgainst: 0
      });
    }

    const stats = teamMap.get(opponent)!;
    stats.played++;

    if (match.result === 'W') {
      stats.wins++;
    } else if (match.result === 'L') {
      stats.losses++;
    } else {
      stats.draws++;
    }

    if (match.isHome) {
      stats.goalsFor += match.homeGoals;
      stats.goalsAgainst += match.awayGoals;
    } else {
      stats.goalsFor += match.awayGoals;
      stats.goalsAgainst += match.homeGoals;
    }
  }

  return Array.from(teamMap.values()).sort((a, b) => b.played - a.played);
}

export function getMatchesByYear(matches: Match[]): Map<number, Match[]> {
  const yearMap = new Map<number, Match[]>();
  
  for (const match of matches) {
    const year = match.year || 0;
    if (!yearMap.has(year)) {
      yearMap.set(year, []);
    }
    yearMap.get(year)!.push(match);
  }
  
  return yearMap;
}

export function getRivalStats(matches: Match[]): { rival: string; wins: number; draws: number; losses: number; total: number }[] {
  const rivalMap = new Map<string, { wins: number; draws: number; losses: number; total: number }>();
  
  for (const match of matches) {
    if (!rivalMap.has(match.opponent)) {
      rivalMap.set(match.opponent, { wins: 0, draws: 0, losses: 0, total: 0 });
    }
    
    const stats = rivalMap.get(match.opponent)!;
    stats.total++;
    
    if (match.result === 'W') stats.wins++;
    else if (match.result === 'L') stats.losses++;
    else stats.draws++;
  }
  
  return Array.from(rivalMap.entries())
    .map(([rival, stats]) => ({ rival, ...stats }))
    .sort((a, b) => b.total - a.total);
}

export function getBiggestWins(matches: Match[], limit: number = 5): Match[] {
  return [...matches]
    .filter(m => m.result === 'W')
    .sort((a, b) => {
      const diffA = a.isHome ? a.homeGoals - a.awayGoals : a.awayGoals - a.homeGoals;
      const diffB = b.isHome ? b.homeGoals - b.awayGoals : b.awayGoals - b.homeGoals;
      return diffB - diffA;
    })
    .slice(0, limit);
}

export function getWorstLosses(matches: Match[], limit: number = 5): Match[] {
  return [...matches]
    .filter(m => m.result === 'L')
    .sort((a, b) => {
      const diffA = a.isHome ? a.awayGoals - a.homeGoals : a.homeGoals - a.awayGoals;
      const diffB = b.isHome ? b.awayGoals - b.homeGoals : b.homeGoals - b.awayGoals;
      return diffB - diffA;
    })
    .slice(0, limit);
}
