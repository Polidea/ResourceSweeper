//
//  ServerAPIClient.m
//  iPokeMon
//
//  Created by Kaijie Yu on 4/1/12.
//  Copyright (c) 2012 Kjuly. All rights reserved.
//

#import "ServerAPIClient.h"

#import "Config.h"
#import "OAuthManager.h"
#import "AFJSONRequestOperation.h"

#pragma mark - Constants
#pragma mark - ServerAPI Constants

// Connection Checking
NSString * const kServerAPICheckConnection = @"/cc";     // /cc:Check Connection
// User
NSString * const kServerAPIGetUserID       = @"/id";     // /uid:User's Unique ID
NSString * const kServerAPIGetUser         = @"/u";      // /u:User
NSString * const kServerAPIUpdateUser      = @"/uu";     // /uu:Update User
NSString * const kServerAPICheckUniqueness = @"/cu";     // /cu:Check Uniqueness
// User's Pokemon
NSString * const kServerAPIGetPokemon      = @"/pm/%d";  // /pm:PokeMon/<PokemonSID:int>
NSString * const kServerAPIGet6Pokemons    = @"/6pm";    // /6pm:SixPokeMons
NSString * const kServerAPIGetPokedex      = @"/pd";     // /pd:PokeDex
NSString * const kServerAPIUpdatePokemon   = @"/upm";    // /upm:Update PokeMon
// pokemon area
NSString * const kServerAPIGetAllPokemonsArea = @"/pma";     // /pma:PokeMon Area
NSString * const kServerAPIGetPokemonArea     = @"/pma/%d";  // /pma:PokeMon Area/<PokemonSID:int>
// Region
// <code> = <cc>:<ca>:<cl>
//   <cc>: code country
//   <ca>: code administrative are
//   <cl>: code locality
NSString * const kServerAPIGetRegion    = @"/r/%@";  // /r:Region/<code>
NSString * const kServerAPIUpdateRegion = @"/ur";    // /ur:Update Region (push new region to server)
// WildPokemon
NSString * const kServerAPIGetWildPokemon = @"/wpm";    // /wp:WildPokeMon
// Map Annotations
NSString * const kServerAPIGetAnnotation = @"/mas/%@"; // /mas:Map AnnotationS/<code>

#pragma mark -
#pragma mark - ServerAPI

@interface ServerAPI ()

// Connection checking
+ (NSString *)_checkConnection;                              // GET
// User
+ (NSString *)_getUserID;                                    // GET
+ (NSString *)_getUser;                                      // GET
+ (NSString *)_updateUser;                                   // POST
+ (NSString *)_checkUniquenessForName;                       // POST
// User's Pokemon
+ (NSString *)_getPokemonWithPokemonID:(NSInteger)pokemonID; // GET
+ (NSString *)_getSixPokemons;                               // GET
+ (NSString *)_getPokedex;                                   // GET
+ (NSString *)_updatePokemon;                                // POST
// Pokemon Area
+ (NSString *)_getAllPokemonsArea;                      // GET
+ (NSString *)_getAreaForPokemonWithSID:(NSInteger)SID; // GET
// Region
+ (NSString *)_getRegionWithCode:(NSString *)code; // GET
+ (NSString *)_updateRegion; // POST
// WildPokemon
+ (NSString *)_getWildPokemon;
// Annotation
+ (NSString *)_getAnnotationWithCode:(NSString *)code; // GET

@end


@implementation ServerAPI
#pragma mark - Public Methods

// Get Server's Root API
+ (NSString *)root {
#ifdef KY_LOCAL_SERVER_ON
  return @"http://localhost:8080";
#else
  return kServerAPIRoot;
#endif
}

// Get url for user ID
+ (NSURL *)getURLForUserID {
  return [NSURL URLWithString:[[self root] stringByAppendingString:kServerAPIGetUserID]];
}

#pragma mark - Private Methods

// Connection checking
+ (NSString *)_checkConnection { return kServerAPICheckConnection; }
// User
+ (NSString *)_getUserID  { return kServerAPIGetUserID; }
+ (NSString *)_getUser    { return kServerAPIGetUser; }
+ (NSString *)_updateUser { return kServerAPIUpdateUser; }
+ (NSString *)_checkUniquenessForName { return kServerAPICheckUniqueness; }

// User's Pokemon
+ (NSString *)_getPokemonWithPokemonID:(NSInteger)pokemonID {
  return [NSString stringWithFormat:kServerAPIGetPokemon, pokemonID];
}

+ (NSString *)_getSixPokemons { return kServerAPIGet6Pokemons; }
+ (NSString *)_getPokedex     { return kServerAPIGetPokedex; }
+ (NSString *)_updatePokemon  { return kServerAPIUpdatePokemon; }

// Pokemon Area
+ (NSString *)_getAllPokemonsArea { return kServerAPIGetAllPokemonsArea; }
+ (NSString *)_getAreaForPokemonWithSID:(NSInteger)SID {
  return [NSString stringWithFormat:kServerAPIGetPokemonArea, SID];
}

// Region
+ (NSString *)_getRegionWithCode:(NSString *)code {
  return [NSString stringWithFormat:kServerAPIGetRegion, code];
}
+ (NSString *)_updateRegion { return kServerAPIUpdateRegion; }

// WildPokemon
+ (NSString *)_getWildPokemon { return kServerAPIGetWildPokemon; }

// Annotation
+ (NSString *)_getAnnotationWithCode:(NSString *)code {
  return [NSString stringWithFormat:kServerAPIGetAnnotation, code];
}

@end

#pragma mark -
#pragma mark - ServerAPIClient

// HTTP headers for request to web server
// Default: |key|, |provider|, |identity|
typedef enum {
  kHTTPHeaderDefault    = 1 << 0,
  kHTTPHeaderWithRegion = 1 << 1  // region
}HTTPHeaderFlag;

@interface ServerAPIClient () {
 @private
  NSString * regionCode_; // record current region code
}

@property (nonatomic, copy) NSString * regionCode;

- (void)_updateHeaderWithFlag:(HTTPHeaderFlag)flag;
- (void)_updateRegion:(NSNotification *)notification;
//- (void)setHTTPHeaderForRequest:(NSMutableURLRequest *)request; // Set HTTP Header for URL request

@end


@implementation ServerAPIClient

@synthesize regionCode = regionCode_;

// singleton
static ServerAPIClient * client_;
+ (ServerAPIClient *)sharedInstance {
  if (client_ != nil)
    return client_;
  
  static dispatch_once_t onceToken;
  dispatch_once(&onceToken, ^{
    client_ = [[ServerAPIClient alloc] initWithBaseURL:[NSURL URLWithString:[ServerAPI root]]];
  });
  return client_;
}

- (void)dealloc {
  self.regionCode = nil;
  [[NSNotificationCenter defaultCenter] removeObserver:self name:kPMNUpdateRegion object:nil];
  [super dealloc];
}

- (id)initWithBaseURL:(NSURL *)url {
  if (self = [super initWithBaseURL:url]) {
    [self registerHTTPOperationClass:[AFJSONRequestOperation class]];
    [self setDefaultHeader:@"Accept" value:@"application/json"];
    [self setDefaultHeader:@"key"    value:kOAuthClientIdentifier];
    
    self.regionCode = @"XX";
    // add observer for notification from |PMLocationManager| when region changed
    [[NSNotificationCenter defaultCenter] addObserver:self
                                             selector:@selector(_updateRegion:)
                                                 name:kPMNUpdateRegion
                                               object:nil];
  }
  return self;
}

#pragma mark - Public Methods

// Method for checking connection to server
- (void)checkConnectionToServerSuccess:(void (^)(AFHTTPRequestOperation *, id))success
                               failure:(void (^)(AFHTTPRequestOperation *, NSError *))failure {
  [self _updateHeaderWithFlag:kHTTPHeaderDefault];
  NSLog(@"Request URL");
  [self getPath:[ServerAPI _checkConnection] parameters:nil success:success failure:failure];
}

#pragma mark - Public Methods: Trainer

// GET userID
- (void)fetchUserIDSuccess:(void (^)(AFHTTPRequestOperation *, id))success
                   failure:(void (^)(AFHTTPRequestOperation *, NSError *))failure {
  [self _updateHeaderWithFlag:kHTTPHeaderDefault];
  NSLog(@"Request UserID");
  [self getPath:[ServerAPI _getUserID] parameters:nil success:success failure:failure];
}

// GET
- (void)fetchDataFor:(DataFetchTarget)target
          withObject:(id)object
             success:(void (^)(AFHTTPRequestOperation *, id))success
             failure:(void (^)(AFHTTPRequestOperation *, NSError *))failure {
  NSString * path;
  if (target & kDataFetchTargetTrainer)
    path = [ServerAPI _getUser];
  else if (target & kDataFetchTargetTamedPokemon)
    path = [ServerAPI _getPokedex];
  else if (target & kDataFetchTargetAllPokemonsArea)
    path = [ServerAPI _getAllPokemonsArea];
  else if (target & kDataFetchTargetPokemonArea)
    path = [ServerAPI _getAreaForPokemonWithSID:[object intValue]];
  else if (target & kDataFetchTargetRegion)
    path = [ServerAPI _getRegionWithCode:self.regionCode];
  else if (target & kDataFetchTargetAnnotation)
    path = [ServerAPI _getAnnotationWithCode:self.regionCode];
  else return;
  
  [self _updateHeaderWithFlag:kHTTPHeaderDefault];
  [self getPath:path parameters:nil success:success failure:failure];
  NSLog(@"Request with URL tail:%@", path);
  
  /*/ *** Legacy ***
   success:(void (^)(NSURLRequest *, NSHTTPURLResponse *, id))success
   failure:(void (^)(NSURLRequest *, NSHTTPURLResponse *, NSError *, id))failure {}   
   
  NSMutableURLRequest * request = [[NSMutableURLRequest alloc] initWithURL:[ServerAPI getUser]];
  [self setHTTPHeaderForRequest:request];
  [request setHTTPMethod:@"GET"];
  NSLog(@"Request URL:%@ --- HTTPHeader:%@", [ServerAPI getUser], [request allHTTPHeaderFields]);
  AFJSONRequestOperation * operation;
  operation = [AFJSONRequestOperation JSONRequestOperationWithRequest:request success:success failure:failure];
  [request release];
  [operation start];
  [self.operationQueue addOperation:operation];*/
}

// POST
- (void)updateData:(NSDictionary *)data
         forTarget:(DataFetchTarget)target
           success:(void (^)(AFHTTPRequestOperation *, id))success
           failure:(void (^)(AFHTTPRequestOperation *, NSError *))failure {
  NSString * path;
  if (target & kDataFetchTargetTrainer)
    path = [ServerAPI _updateUser];
  else if (target & kDataFetchTargetTamedPokemon)
    path = [ServerAPI _updatePokemon];
  else if (target & kDataFetchTargetRegion)
    path = [ServerAPI _updateRegion];
  else return;
  
  [self _updateHeaderWithFlag:kHTTPHeaderDefault];
  NSLog(@"Sync Data Request");
  [self postPath:path parameters:data success:success failure:failure];
}

// POST: Check uniqueness for the |name|
- (void)checkUniquenessForName:(NSString *)name
                       success:(void (^)(AFHTTPRequestOperation *operation, id responseObject))success
                       failure:(void (^)(AFHTTPRequestOperation *operation, NSError *error))failure {
  [self _updateHeaderWithFlag:kHTTPHeaderDefault];
  NSLog(@"Request URL...");
  [self postPath:[ServerAPI _checkUniquenessForName]
      parameters:[NSDictionary dictionaryWithObject:name forKey:@"name"]
         success:success
         failure:failure];
}

#pragma mark - Public Methods: WildPokemon

// Update data for Wild Pokemon at current Region
//   |regionInfo|:
//                 { "t"(type):XXX, ... }
- (void)updateWildPokemonsForCurrentRegion:(NSDictionary *)regionInfo
                                   success:(void (^)(AFHTTPRequestOperation *, id))success
                                   failure:(void (^)(AFHTTPRequestOperation *, NSError *))failure {
  [self _updateHeaderWithFlag:kHTTPHeaderDefault | kHTTPHeaderWithRegion];
  [self getPath:[ServerAPI _getWildPokemon]
     parameters:regionInfo
        success:success
        failure:failure];
}

#pragma mark - Provate Methods

- (void)_updateHeaderWithFlag:(HTTPHeaderFlag)flag {
  // Reset headers to empty
  [self setDefaultHeader:@"provider" value:nil];
  [self setDefaultHeader:@"identity" value:nil];
  [self setDefaultHeader:@"region"   value:nil];
  
  // Default headers
  if (flag & kHTTPHeaderDefault) {
    [self setDefaultHeader:@"provider" value:
      [NSString stringWithFormat:@"%d",
        [[NSUserDefaults standardUserDefaults] integerForKey:kUDKeyLastUsedServiceProvider]]];
    [self setDefaultHeader:@"identity" value:[[OAuthManager sharedInstance] userEmailInMD5]];
  }
  
  // Include user location info if needed
  if (flag & kHTTPHeaderWithRegion) [self setDefaultHeader:@"region" value:@"1"];                      
}

// update region (code, ...)
- (void)_updateRegion:(NSNotification *)notification {
  self.regionCode = notification.object;
}

// Set HTTP Header for URL request
//- (void)setHTTPHeaderForRequest:(NSMutableURLRequest *)request {
//  NSString * provider = [NSString stringWithFormat:@"%d",
//                         [[NSUserDefaults standardUserDefaults] integerForKey:kUserDefaultsLastUsedServiceProvider]];
//  [request setValue:@"123456" forHTTPHeaderField:@"key"];
//  [request setValue:provider forHTTPHeaderField:@"provider"];
//  [request setValue:[[OAuthManager sharedInstance] userEmailInMD5] forHTTPHeaderField:@"identity"];
//}

@end
