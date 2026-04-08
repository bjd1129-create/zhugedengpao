export interface GameData {
    playerName: string;
    currentLevel: number;
    stars: number[];
    codeFragments: number;
    playTime: number;
    achievements: string[];
}
export declare function saveGame(data: GameData): void;
export declare function loadGame(): GameData | null;
export declare const GAME_CONSTANTS: {
    TOTAL_LEVELS: number;
    HIDDEN_LEVELS: number;
    CODE_FRAGMENTS_FOR_SKIN: number;
    CODE_FRAGMENTS_FOR_OUTFIT: number;
    CODE_FRAGMENTS_FOR_HIDDEN: number;
};
//# sourceMappingURL=main.d.ts.map