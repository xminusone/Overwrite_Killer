import praw, time, datetime, traceback, obot
#obot is used to login with OAuth, you will get an exception if you attempt to import it

"""
Remove and tempban script users.
"""

#login using file with oauth app details
r = obot.login()

#create empty arrays so we don't act on things twice
recentlyDonePosts = []
recentlyBannedUsers = []
recentlyModdedSubs = []

botActive = True

#get posts from /r/mod
rmod = r.get_subreddit("mod")


#string sent to user
sentToUserString = "You have been temporarily banned for using a comment overwrite script. This is considered spam. In future, please use a less spammy overwrite message. Thank you."

def is_banned(sub, user):
    if [i for i in list(r.get_banned(sub)) if i.name == user]:
        return True
    return False

#post checker method
def check():
        #NOTE: I modified praw (not my modification) in order to allow for edited sort, so this won't work for you natively!
        #To add this yourself, see: http://redd.it/2y2rvj
        stream = rmod.get_edited(limit=100)
        #this phrase is always found in the comments
        scriptKeyword = "This comment has been overwritten by"
        #make sure we get the right thing
        for comment in stream:
            try:
                text = comment.body
            except AttributeError:
                text = comment.selftext
            if scriptKeyword in text and comment.id not in recentlyDonePosts:
                if comment.banned_by == None:
                        #string for mod note
                        subofcomment = comment.subreddit
                        modString = "Greasemonkey overwrite script:", comment.id
                        
                        if comment.author == None:
                            cmtAuthor = "[deleted]"
                        else:
                            cmtAuthor = comment.author.name
                        #ban args
                        banargs = {"duration": 3, "note": modString, "ban_message": sentToUserString}
                        
                        #remove the comment regardless
                        comment.remove(spam=False)
                        print("Removed id " + comment.id + " by " + cmtAuthor + " from /r/" + comment.subreddit.display_name)
                        recentlyDonePosts.append(comment.id)
                        #don't bother banning them if they're already banned
                        
                        try:
                            if is_banned(subofcomment, cmtAuthor) or cmtAuthor in recentlyBannedUsers:
                                pass
                            else:
                                if cmtAuthor == "[deleted]":
                                    pass
                                else:
                                    rmod.add_ban(subofcomment, **banargs)
                                    recentlyBannedUsers.append(cmtAuthor)
                                    print("Tempbanned " + cmtAuthor + " in " + "/r/" + comment.subreddit.display_name)
                        except:
                            recentlyBannedUsers.append(cmtAuthor)
                            print("Couldn't ban " + cmtAuthor + " from /r/" + comment.subreddit.display_name + ". No access permission?")
                        
                        
                        
        #let's relax a little
        time.sleep(1)
def getTime():
    currentSysTime = time.localtime()
    return time.strftime('%m/%d/%y @ %H:%M:%S', currentSysTime)
while True:
    try:
        check()
    except:
        time.sleep(10)

