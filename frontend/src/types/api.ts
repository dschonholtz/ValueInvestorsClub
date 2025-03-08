export interface Idea {
  id: string;
  link: string;
  company_id: string;
  user_id: string;
  date: string; // ISO date string
  is_short: boolean;
  is_contest_winner: boolean;
}

export interface Company {
  ticker: string;
  company_name: string;
}

export interface User {
  username: string;
  user_link: string;
}

export interface Description {
  description: string;
}

export interface Catalysts {
  catalysts: string;
}

export interface Performance {
  nextDayOpen: number | null;
  nextDayClose: number | null;
  oneWeekClosePerf: number | null;
  twoWeekClosePerf: number | null;
  oneMonthPerf: number | null;
  threeMonthPerf: number | null;
  sixMonthPerf: number | null;
  oneYearPerf: number | null;
  twoYearPerf: number | null;
  threeYearPerf: number | null;
  fiveYearPerf: number | null;
}

export interface IdeaDetail extends Idea {
  company?: Company;
  user?: User;
  description?: Description;
  catalysts?: Catalysts;
  performance?: Performance;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
}

export interface ListParams {
  skip?: number;
  limit?: number;
  company_id?: string;
  user_id?: string;
  is_short?: boolean;
  is_contest_winner?: boolean;
  start_date?: string;
  end_date?: string;
  search?: string;
}