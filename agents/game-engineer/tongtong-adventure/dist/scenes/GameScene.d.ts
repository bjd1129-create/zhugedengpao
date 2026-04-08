import Phaser from 'phaser';
interface GameSceneData {
    level: number;
}
export declare class GameScene extends Phaser.Scene {
    private levelData;
    private currentLevel;
    private inputText;
    private feedbackText;
    private hintIndex;
    private score;
    private currentAnswer;
    constructor();
    init(data: GameSceneData): void;
    private loadLevelData;
    create(): void;
    private showTutorial;
    private checkAnswer;
    private showHint;
    private celebrate;
    private nextLevel;
    private showChapterComplete;
    private backToMenu;
}
export {};
//# sourceMappingURL=GameScene.d.ts.map