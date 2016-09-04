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
sentToUserString = "Greetings!  Your comment has been automatically removed because it is spam.  Spamming is a really shitty thing to do.  This script is one of the dumbest and spammiest scripts that I have ever seen.  Did you know that no one cares about your mundane comments?  You actually aren't even protecting any privacy because there are many sites out there that specifically cache comments just so that users cannot edit them.\n\nTo reiterate, this script is shit and you should not be using it.  Search for a different one, or edit it to say something less spammy.  But in the end, it won't matter because we can still see whatever it was that you edited.\n\nYou should also read this: https://reddit.zendesk.com/hc/en-us/articles/204536499-What-constitutes-spam-Am-I-a-spammer- \n\nDid I mention that is spammy and we don't like it?"

def is_banned(sub, user):
    if [i for i in list(r.get_banned(sub)) if i.name == user]:
        return True
    return False

#post checker method
def check():
        #NOTE: I modified praw (not my modification) in order to allow for edited sort, so this won't work for you natively!
        stream = praw.helpers._stream_generator(rmod.get_edited, 100)
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
                            if is_banned(rmod, cmtAuthor.name) or cmtAuthor.name in recentlyBannedUsers:
                                pass
                            else:
                                if cmtAuthor == "[deleted]":
                                    pass
                                else:
                                    rmod.add_ban(cmtAuthor, **banargs)
                                    recentlyBannedUsers.append(cmtAuthor.name)
                                    print("Tempbanned " + cmtAuthor.name + " in " + "/r/" + comment.subreddit.display_name)
                        except:
                            recentlyBannedUsers.append(cmtAuthor.name)
                            print("Couldn't ban " + cmtAuthor.name + " from /r/" + comment.subreddit.display_name + ". No access permission?")
                        
                        
                        
        #let's relax a little
        time.sleep(1)
def getTime():
    currentSysTime = time.localtime()
    return time.strftime('%m/%d/%y @ %H:%M:%S', currentSysTime)
while True:
    try:
        check()
    except:
        time.sleep(1)

