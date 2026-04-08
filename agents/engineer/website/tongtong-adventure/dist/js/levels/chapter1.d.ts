export interface PuzzleData {
    level: number;
    type: string;
    question: string;
    answer: number;
    hints: string[];
    difficulty: number;
    reward: number;
}
export declare const CHAPTER_1_LEVELS: PuzzleData[];
export declare function getLevelData(level: number): PuzzleData | undefined;
export declare const CHAPTER_1_INFO: {
    chapter: number;
    chapterName: string;
    totalLevels: number;
    theme: string;
    color: number;
};
//# sourceMappingURL=chapter1.d.ts.map