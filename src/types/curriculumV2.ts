export type RoiTier = 'S-tier' | 'A-tier' | 'B-tier' | 'C-tier' | 'Niche';

export interface CuratedProblem {
  id: string;
  name: string;
  platform: string;
  rating: number;
  url: string;
  insight: string;
  tags: string[];
}

export interface ExternalLink {
  title: string;
  url: string;
  source: string;
}

export interface CurriculumV2Topic {
  id: string;
  title: string;
  sectionId: string;
  sectionTitle: string;
  phaseId: number;
  phaseName: string;
  icon: string;
  sourceFile: string;
  roi: RoiTier | string;
  frequency: string;
  ratingRange: string;
  prerequisites: string;
  whyItMatters: string;
  coreIntuition: string;
  recognitionPatterns: string[];
  derivation: string;
  templateCpp: string;
  templatePython: string;
  complexity: string;
  commonBugs: string[];
  variants: string;
  problemPatterns: string;
  recognitionExercises: string;
  cheatSheet: string;
  externalLinks?: ExternalLink[];
  curatedProblems?: CuratedProblem[];
}

export interface CurriculumV2Module {
  id: string;
  sectionNumber: number;
  sectionId: string;
  title: string;
  shortTitle: string;
  phaseId: number;
  phaseName: string;
  icon: string;
  summary: string;
  topicsCount: number;
  topics: CurriculumV2Topic[];
  externalLinks?: ExternalLink[];
  curatedProblems?: CuratedProblem[];
}

export interface CurriculumV2Phase {
  id: number;
  number: number;
  name: string;
  shortName: string;
  badge: string;
  color: string;
  description: string;
  sections: string[];
}

export interface CurriculumV2Track {
  id: string;
  name: string;
  ratingRange: string;
  badge: string;
  color: string;
  description: string;
  sections: string[];
}

export interface RoiMapEntry {
  topic: string;
  roi: string;
  frequency: string;
  difficulty: string;
  prerequisites: string;
  ratingRange: string;
}

export interface CheatSheetSubtopic {
  topic: string;
  recognitionClue: string;
  coreIdea: string;
  complexity: string;
  mainTemplate: string;
  commonUseCase: string;
  sectionFile: string;
}

export interface CheatSheetSection {
  sectionTitle: string;
  subtopics: CheatSheetSubtopic[];
}

export interface CurriculumV2Data {
  metadata: {
    title: string;
    subtitle: string;
    version: string;
    totalModules: number;
    totalTopics: number;
    totalTemplates: number;
    roiDistribution: Record<string, number>;
  };
  phases: CurriculumV2Phase[];
  tracks: CurriculumV2Track[];
  modules: CurriculumV2Module[];
  roiMap: RoiMapEntry[];
  cheatSheet: CheatSheetSection[];
}
