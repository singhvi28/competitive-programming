export interface MirrorSubmissions {
  'a.out'?: string;
  'Queue'?: string;
  [key: string]: string | undefined;
}

export interface MirrorRawProblem {
  contest_id: number;
  index: string;
  problem_id: string;
  name: string;
  rating: number;
  tags?: string;
  problem_link: string;
  submission_link?: string;
  user?: string;
  solved_by: ('a.out' | 'Queue' | string)[];
  submissions: MirrorSubmissions;
}
