import Phaser from 'phaser';
export declare class GameScene extends Phaser.Scene {
    private levelData;
    private codeFragments;
    private stars;
    private currentHintIndex;
    private attempts;
    private answerInput;
    private submitButton;
    private hintButton;
    private feedbackText;
    private hintDisplay;
    constructor();
    init(data: {
        level: number;
    }): void;
    create(): void;
    private handleInput;
    private checkAnswer;
    private showHint;
    update(): void;
    saveProgress(stars: number, fragments: number): void;
}
//# sourceMappingURL=GameScene.d.ts.map