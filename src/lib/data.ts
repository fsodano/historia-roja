import type { Match, MatchStats, TeamStats } from './types';

export function parseMatches(): Match[] {
  const rawData = `Independiente	1	4	Racing Club	L
Argentinos Juniors	1	1	Independiente	V
Independiente	3	1	Huracán	L
Lanús	0	2	Independiente	V
Independiente	2	3	Boca Juniors	L
Independiente	6	1	Atlanta	L
Estudiantes	5	2	Independiente	V
Independiente	1	0	Talleres (RE)	L
River Plate	1	0	Independiente	V
Independiente	1	1	Chacarita Juniors	L
Gimnasia (LP)	2	1	Independiente	V
Independiente	1	1	Quilmes	L
Ferro Carril Oeste	1	1	Independiente	V
San Lorenzo	1	1	Independiente	V
Independiente	2	0	Platense	L
Tigre	1	4	Independiente	V
Independiente	1	0	Vélez Sarsfield	L
Racing Club	7	4	Independiente	V
Independiente	3	2	Argentinos Juniors	L
Huracán	5	1	Independiente	V
Independiente	4	1	Lanús	L
Boca Juniors	1	1	Independiente	V
Atlanta	0	1	Independiente	V
Independiente	3	2	Estudiantes	L
Talleres (RE)	3	0	Independiente	V
Independiente	2	1	River Plate	L
Independiente	1	1	Gimnasia (LP)	L
Quilmes	1	2	Independiente	V
Independiente	2	1	Ferro Carril Oeste	L
Independiente	5	3	San Lorenzo	L
Platense	4	1	Independiente	V
Independiente	3	2	Tigre	L
Vélez Sarsfield	2	3	Independiente	V
Huracán	2	1	Independiente	V
Independiente	3	0	Atlanta	L
Boca Juniors	0	2	Independiente	V
Independiente	2	0	Lanús	L
Independiente	1	1	San Lorenzo	L
Ferro Carril Oeste	2	4	Independiente	V
Independiente	2	0	Tigre	L
Argentinos Juniors	3	4	Independiente	V
Independiente	1	1	Estudiantes	L
Ferro Carril Oeste	2	4	Independiente	V
Independiente	4	0	Quilmes	L
Platense	2	0	Independiente	V
Gimnasia (LP)	2	2	Independiente	V
Independiente	2	0	Vélez Sarsfield	L
Talleres (RdE)	1	2	Independiente	V
Independiente	5	0	River Plate	L
Racing Club	0	2	Independiente	V
Independiente	3	2	Huracán	L
Atlanta	0	1	Independiente	V
Independiente	2	1	Boca Juniors	L
Lanús	0	0	Independiente	V
San Lorenzo	2	2	Independiente	V
Independiente	2	1	Chacarita Juniors	L
Tigre	2	3	Independiente	V
Independiente	1	0	Argentinos Juniors	L
Estudiantes	1	1	Independiente	V
Independiente	2	1	Ferro Carril Oeste	L
Quilmes	3	1	Independiente	V
Independiente	4	0	Platense	L
Independiente	1	2	Gimnasia (LP)	L
Vélez Sarsfield	0	0	Independiente	V
River Plate	6	1	Independiente	V
Independiente	0	1	Racing Club	L
Independiente	1	0	River Plate	L
Racing Club	2	1	Independiente	V
Independiente	3	1	Huracán	L
Quilmes	0	1	Independiente	V
Independiente	6	3	Platense	L
Estudiantes (LP)	0	0	Independiente	V
Vélez Sarsfield	2	0	Independiente	V
Independiente	7	0	Tigre	L
Argentinos Juniors	1	0	Independiente	V
Independiente	2	1	Gimnasia (LP)	L
Ferro Carril Oeste	1	2	Independiente	V
Independiente	4	0	Atlanta	L
Talleres (RdE)	3	0	Independiente	V
Independiente	1	1	Boca Juniors	L
Independiente	2	1	Chacarita Juniors	L
San Lorenzo	2	0	Independiente	V
Independiente	3	3	Lanús	L
River Plate	1	1	Independiente	V
Independiente	2	0	Quilmes	L
Platense	2	1	Independiente	V
Tigre	1	3	Independiente	V
Independiente	3	1	Argentinos Juniors	L
Independiente	1	0	San Lorenzo	L
Atlanta	0	2	Independiente	V
Independiente	3	2	Talleres (RdE)	L
Boca Juniors	2	0	Independiente	V
Independiente	0	0	Estudiantes (LP)	L
Independiente	3	2	Ferro Carril Oeste	L`;

  const lines = rawData.trim().split('\n');
  const matches: Match[] = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;

    const parts = line.split('\t');
    if (parts.length !== 5) continue;

    const [team1, goals1Str, goals2Str, team2, location] = parts;
    const goals1 = parseInt(goals1Str);
    const goals2 = parseInt(goals2Str);
    
    const isIndependienteHome = team1 === 'Independiente';
    
    let independienteGoals: number;
    let opponentGoals: number;
    let opponent: string;
    
    if (isIndependienteHome) {
      independienteGoals = goals1;
      opponentGoals = goals2;
      opponent = team2;
    } else {
      independienteGoals = goals2;
      opponentGoals = goals1;
      opponent = team1;
    }
    
    let result: 'W' | 'L' | 'D';
    if (independienteGoals > opponentGoals) {
      result = 'W';
    } else if (independienteGoals < opponentGoals) {
      result = 'L';
    } else {
      result = 'D';
    }
    
    const match: Match = {
      id: `match-${i}`,
      homeTeam: team1,
      awayTeam: team2,
      homeGoals: goals1,
      awayGoals: goals2,
      isHome: isIndependienteHome,
      result: result,
      opponent: opponent
    };

    matches.push(match);
  }

  return matches;
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