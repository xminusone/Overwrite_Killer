import praw, time, datetime, traceback, obot
#obot is the file used to login with OAuth

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
def check(stream):
        #this phrase is always found in the comments
        scriptKeyword = "This comment has been overwritten by"
        #NOTE: I modified praw (not my modification) in order to allow for edited sort, so this won't work for you natively!
        for comment in stream:
            text = comment.body
            if scriptKeyword in text and comment.id not in recentlyDonePosts:
                if comment.banned_by == None:
                        #string for mod note
                        modString = "Greasemonkey overwrite script:", comment.id
                        
                        cmtAuthor = comment.author
                        #ban args
                        banargs = {"duration": 3, "note": modString, "ban_message": sentToUserString}
                        
                        #remove the comment regardless
                        comment.remove(spam=False)
                        print("Removed id " + comment.id + " by " + cmtAuthor.name + " from /r/" + comment.subreddit.display_name)
                        recentlyDonePosts.append(comment.id)
                        #don't bother banning them if they're already banned
                        if is_banned(rmod, cmtAuthor.name) or cmtAuthor.name in recentlyBannedUsers:
                                pass
                        else:
                                rmod.add_ban(cmtAuthor.name, **banargs)
                                recentlyBannedUsers.append(cmtAuthor.name)
                                print("Tempbanned " + cmtAuthor.name + " in " + "/r/" + comment.subreddit.display_name)
                        
                        
                        
        #let's relax a little
        time.sleep(1)
def getTime():
    currentSysTime = time.localtime()
    return time.strftime('%m/%d/%y @ %H:%M:%S', currentSysTime)

try:
    while True:
        stream = praw.helpers._stream_generator(rmod.get_edited, 100)
        check(stream)
except:
    print("Exception. Sleeping for 2 minutes.")
    tine.sleep(120)

