export interface Match {
  id: string;
  homeTeam: string;
  awayTeam: string;
  homeGoals: number;
  awayGoals: number;
  isHome: boolean;
  result: 'W' | 'L' | 'D';
  opponent: string;
}

export interface MatchStats {
  totalMatches: number;
  wins: number;
  losses: number;
  draws: number;
  goalsScored: number;
  goalsConceded: number;
  goalDifference: number;
  winPercentage: number;
}

export interface TeamStats {
  team: string;
  played: number;
  wins: number;
  losses: number;
  draws: number;
  goalsFor: number;
  goalsAgainst: number;
}