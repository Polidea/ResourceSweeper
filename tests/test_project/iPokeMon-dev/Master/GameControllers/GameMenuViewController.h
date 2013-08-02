//
//  GameMenuViewController.h
//  iPokeMon
//
//  Created by Kaijie Yu on 2/26/12.
//  Copyright (c) 2012 Kjuly. All rights reserved.
//

#import <UIKit/UIKit.h>

@protocol GameMenuViewControllerDelegate;

@interface GameMenuViewController : UIViewController <UIAlertViewDelegate> {
  id <GameMenuViewControllerDelegate> delegate_;
}

@property (nonatomic, assign) id <GameMenuViewControllerDelegate> delegate;

- (void)prepareForNewScene;
- (void)reset;

@end


// Delegate

@protocol GameMenuViewControllerDelegate

- (void)unloadBattleScene;

@end
