from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()
    
# create sample documents
"""doc_a = "New interface The options menu at the bottom was good and easy to use. This new version with many changes which I think is not better than the old version. 3 stars for this new version just because I like this file manager."
doc_b = "Version expires!! Oh wait.. after being pissed about the expired code i uninstalled it and then install it again and they updated it already.. no more version expires in 2 days yaay thanks"
doc_c = "cannot send requests to Facebook I was happy with the app before the update. Now I cannot send new requests for birthdays to people on Facebook. Also the pop-ups can be quite annoying. They're very loud and random, before you know it you are redirected to that app slowing down loading The calendar"
doc_d = "notifications my main gripe is i get a notification of 1 friend's birthday but when I check on the app its displaying a red highlight with no-one listed is this a bug??."
doc_e = "cannot sign in I have tried to sign in 6 times I forgot my pin and requested help. Temporary pin was supposed to be sent to email and after six times I give. I could make my own in this much time" 
doc_f = "Love it Everything in one place. Plus it takes me right to the IRS web page so I can check my refund status. A+"
doc_g = "So far the best Easy to use app. It let you know if mistakes or IRS rejection and it provides the solution before resubmit."
doc_h = "Useful App appears to have the information needed right at hand"""
documents = [
             " I am almost afraid to say this because every time I have an app ends up closing down but keep up the good work This is the most useful Bible offline that I have found on the market. I was having a problem finding one that did not try to direct me into what I should study and I was having a problem finding enough versions. And it was pretty annoying until I found this one. I like that it has a lot of versions and a lot of different languages so that I can  it helps to share the gospel to people who dont speak my language. Thanks and dont go anywhere. More versions please!  :)"   ,
             " Offline is great! However, the audio is the worst. It has that robotic sound which is so hard to listen to, and annoying mind u. I love the voices of real ppl, the kind that put inflexion in the voice. Otherwise great app."   ,
             " Good but for very insisting rate me popup User selected verse by verse comparison of different Bibles in either different colors or fonts . (if not already installed, didn't get real chance to test app- was still loading versions when rate me kept popping up after each install press) make it so you can select all the versions  you want then press install to save time.  An option to transfer app to another device without redoing downloads again or a Google sync fuction that when downloaded on another device it automatically downloads your choices."   ,
              "Love this app! Love how easy it is to use. it is great to be able to highlight verses with different colors for different reasons. Thanks Bible Offline! Be blessed and keep honoring God."   ,
             "WORSHIP 24/7 This app is the best! Especially for us people who like to make excuses not to read the bible. I myself use to say I didn't have time,but this app and it is accurate Old King James version has allowed me to read my 10 chapters a day with no problem. Whether I read it all at once or in pieces I still am able to read the word on my busy  schedule. This App has DEFINITELY helped me strengthen my faith in the LORD. God bless the people who put their time and effort into making this app. HIGHLY Recommend."   ,
              "Bible Offline They advertised the app was free, but now they are wanting me to pay. The price is not much, but, to me, it seems underhanded, and dishonest to pull such a bait and switch.  I will erase it."   ,
              "WONDERFUL AND USEFUL APP This app helps me to maintain a daily bible reading plan. Its search function is so wonderful. I can make my notes and comments as i read. it is a great app; a must have for lovers of God's word. Moreover, it comes handy when i travel to a place where there is no internet connection."   ,
             " The app is beautifully done! Since the new update the UI looks beautifully done.When I want to read the bible on the go, this app is perfect! With night mode, the app is easy to the eyes! It has a widget that gives me a daily dose of bible quotings! Would recommend to anyone"   ,
            " The Best Offline Bible App This is the best Bible reading app I have ever used and I have tried many.  The other Bible apps left me frustrated &  disappointed because they didn't work offline or didn't function consistently.  This app works every time and it works offline.  I can take notes, bookmark and highlight with it.  I gladly paid to remove advertising and now this app is so awesome....I love this Bible app."   ,
             "Inspiration Not only is it easy and convenient to use , it also inspires me each ad every day. #useful"   ,
             " Thanks from my heart. Love all the modern features that a great bible app needs for inspiration, study, prayer etc. and all things nice, Jesus loves yous :-)"   ,
             "First Bible application that I have used. This app is very easy to use and is excellent for studying God's word! This is the absolute sharpest sword that I have ever experienced and, it has completely cut away the evil demons that had been attached to my soul and has freed me from a lifetime of all of the torture, pain, suffering, abusement by everyone in my whole life. God and his son(my saviour) is my only family and can trust in them. They are also the only ones that truly love me!"   ,
             " THE BIBLE OFF LINE SO LOVELY May the Lord bless and strengthen you for this soul winning and inspiring work. The lazy and careless, even unbelievers have been inspired through this wonderful work and are daily giving their lives to Christ. Thanks for making this Bible comprehensive and easily accessible."   ,
             " Upgrade is awesome I love the fact that I can now download all the versions that I want and it STAYS downloaded. I had a problem before where it would only download 1 version at a time. The audio reader sounds more human too. This app has been great since I downloaded it. Its even better since the upgrade. My suggestions so far is that you fix the search (sometimes it says No verse found when the word is actually there - please test) and yes the maps could include journeys other than Paul's."   ,
             " Best, Sensible, Realistic, and truly GOD inspired it is a real bible. From navigation , bookmarks, font adjust, and a particular feature that's important. (The heading dont move) whilst reading.  so that you always know which book and chapter yore reading. And all the other wonderful features. Keep it up guys, and keep on trusting in the one and only, our LORD, GOD of our salvation, YESHUA, Jesus the CHRIST, whom is soon to come. Amen."   ,
             " cannot access audible bible Purchased the audible bible on my Samsung note 3 but cannot access it. When I click restore purchase it says, successfully restored, but still I cannot access it. Please help"   ,
             " Excellent! Awesome App for the very nearsighted Love it!!! I can make the font as large as I need!!!!!   Awesome high contrast text with night mode and several font styles.  i am able to tune easily for my nearsighted oddball eyeballs. Thank you so much. If I dont feel like reading the app will read it out loud to me."   ,
              "Excellent scripture source I use this scripture app on all m touch screen devices. It is very simple to use, you can navigate through the books, chapters and verses with relative ease. I especially like the fact that you can highlight and bookmark the verses that are pertinent to you. Very handy. I also like the fact that the app doesnt take long to load. I have recommended it to several friends.  The best scripture app for me."   ,
              "LOVE THIS APP! I absolutely love this app! it is very easy to use and I really appreciate the fact that I can use it offline, and not use up a ton of data. I also love the fact that there are several versions of the Bible that can be  downloaded  as well.  it is really good for those who like to study the Word of God using various texts. It is such a blessing to be able to take God's Word with me every where I go. Many Blessings to you for sharing this great resource."   ,
             " Best of the Bible apps I have tried Easy to use, can mark my passages for quickly finding later.  Can easily look up passages to keep up with sermons"   ,
             "Cannot sort books There is no option to sort books into an orderly fashion. This app needs a bookshelf where you can arrange the books into folders or categories. Who wants al+A58l their books, magazines, recipes, work documents, fictions, reference books all jumbled all together? No one. This is a basic feature. Please sort this."   ,
               "This App is a Must Have , and in all my time spent on it. i haven't found a single bug or discrepancy... download right away!!"   ,
              "Part time job... Part time job...!!    Monthly payment Guaranteed...!!    Just install Champcash....!! SEARCH CHAMPCASH EARN MONEY On Playstore  And CHAMPCASH APP INSTALL Karne Ke Baad *SIGNUP WITH CHAMPCASH Kare. Please Join Our Team Refer *Sponsor ID 2531059 and Join  Me _Earn Rs. 1,000+/-a Day As Part_Time/Full Time Job So dont Waste Your Time  Install Hurry Up. After Installation Sign up karne k baad jab Sponsor Id maange to ID 2531059 daal dena is App se Aap Meri Team me Join ho ke and *Challenge Complete Karke **50,000/- Per Month kma sakte hai . *CHAMPCASH ID 2531059"   ,
              "Unfortunately google play book stopped I have updated my os to android 6 after updates google play books didn't works properly automatically the app closed"   ,
             " False advertisement I wanted to try this app and grabbed some random free book. Then I was asked for my credit card information. If I go for a walk I dont expect to be stopped and asked to show my wallet. Yes, sir, walking is free. But what if you decide to buy something? Well, this store is one place i am not spending any money EVER."   ,
              "The app is not working When I upgraded my phone from lollipop to marshmallow it stopped working.... And the message 'Unfortunately, Google play books has stopped' comes again again whenever I start using Internet connection"   ,
              "Google Play Books has stopped working.. !! This message repeatedly pop-ups on my screen even when i dont open it. When i click on report it, it doesnt respond. Help out with a solution. Please. "  ,
             " Only two concerns Just if google can add an offline reading support without the need to upload every book to the cloud by letting the user browse his/her local library, ALSO this annoying blue symbol that stucks on the book after it being downloaded forever...it have to be clean af instead of putting some annoying stickers."   ,
             " Awesome I like the app, it is interface is stable and can turn PDFs to night mode(which is a big plus). The only thing I consider that is quite annoying is the fact that I have to put my credit card to download free books."   ,
              " Still stops reading alound while the screen is locked! Defeats the whole point of it! Apparently the only reason this application has read aloud is so that developers or PM can say it is supported on the feature list."   ,
              "PLEASE FIX!!!!!! App stop working it says that no Internet please check connection. My internet works fine for everything else so it has to be this app. I bought book I would like to read them. They won't even upload. Not even with data pack. I even true another internet connect with no luck. Try what you said even tried removing x-memory and did not help either. I am not the only one having this problem."   ,
             " Very disappointed with this app. In my phone google play books is not responding. Every time I open any app, or playing games, or doing some work, taking picture a pop up come up and saying google play is not unfortunately not working.with option of ok and report. When i press report button they dont send any report. And for some time it dont come out.and after some time, then again it come to irritate. Please help me google."   ,
              "!?!NewGlitch2016 0219 Read article Twitter &dowhatHavDone1000Times&go2save2DRIVE&AUTO shifted me into GooglePlayBooks&tells me pdf will be saved there4offLineReading but but... WHY???  //////  2015- ?!? Ok, Google re-enabledPurchasd Library Download to SD-Card 4 OffLine read BUT BOOKMARK back stepd2 [blah blah blah.. ] Many thx 4 fix moving to SD-CARD!"   ,
             " Annoying upload and pdf viewer it is another app Google has forgotten it seems. Unfortunately there is no custom sort feature but most disappointing is the frequent downloading and uploading. I have a lot of my books on a SD card why the hell do I need to upload then re-download just to read a book. Classic Google issue of overthinking how it is apps are used by users."   ,
             " App isn't working Whenever I open the app, dialog came up on screen showing unfortunately Google play books has stopped. Please help me to figure it out .."   ,
             " Nexus7tablet Prices are getting better now, and nice to see alot more free books on my recommended, used to love this site heading back to it getting better, good work guys"   ,
              "Awesome but just one suggestion First off, I love reading books on my phone and I love the new night light option. But, PLEASE add a manual option for nightlight rather than always being automatically enabled only during the night. I work night shift, and when I get off work and want to read a little bit, it would be great to be able to use that function. Please consider that, thanks."   ,
             " Best ebook reading app Have tried some others but Play Book is over all the best - reading experience and useful features. Saw some people complained and annoyed at the need for uploading book to cloud and then downloading for offline reading. This is because they do not understand and/or do not interest in the concept of being able to read the same book (and library of books) including all its settings/annotations across devices which is a really nice feather."   ,
              "doesnt sync I use this app on both my galaxy s6 and my tab 4 but you cannot sync them together to pick up where one device left off. it is really frustrating. Thinking of switching to a different app."   ,
             " I love it It has become one of my favorites apps. It has a nice set of options to config, it is very reliable and it is easy to use."   ,
             " it is good- yore not syncing It makes studying easier and highlighting with notes is an awesome idea. It isn't syncing with my phone and tablets. Please fix. Now, i am upset. I had a part of my magazine studied and now, it is totally erased. I even had notes. What happened?"   ,
              "Read PDF from device Nice App but It looks like Google app developers unable to make reading PDF from local Drive ,unnecessary have to upload and then need to download from cloud. Is it look like user friendly?"  ,
            " I like it but i am annoyed The app does what it is supposed to, let's you read books on your phone. But I've in countered a very annoying problem. When using orignal pages, instead of flowing text, I am unable to use page links, url links, and text selection for highlighting. If I use flowing text and highlight somthing then on original text, the highlight is no where near the text and is some were in the middle of the page (or were some were else depending on the text but it still wrong)"   ,
              "Needs a few features Please give us the option for creating folders for books. Also needs the option to change sort orders to sort books by publication date or some other custom sort.  *Update* Lowering score - too much time has passed and still no folders or advanced sort options.  :(  " ,
             " All good..  Except one thing.. Everything is perfect except one thing.. Please add option to upload books directly from google drive mobile app.  Every time when I want to upload new book which I already have in my Drive,  either I need to go to web link of play books or download book from drive to mobile and then upload it again to playbooks which unnecessarily waste lot of time.."   ,
              "Less is more Google proves I love the clean design and simplicity of this app. Makes for a great reading experience. The only thing missing is PDF support, which I hope Google will add soon."   ,
               "I've been using Cool Reader for years but decided to try this reader because of various crashing reasons :-) It allowed me to use volume buttons for page turns.  Very nice. However. I am losing my place mark if I want to switch from day to night, or when I set display brighter. Finally realised the settings and chapter buttons are much to close to each other. An easier (hint:some gesture)  way to get display dimmed would be appreciated. Ps. I only tried epub so far.. Update - 2015 - I have to many ebooks - management is a pain - started using Allreader"   ,
             " I cannot its worst Any the ducking books I read now today its marsh fuffy I cannot log in its hard work to do i went to high school today my games doesnt work. Even i play cute games my wallpapers are ainme now faster I am"   ,
              "Awesome, but... I love the app, I think it is really easy to use, and the options you have are helpful. However, I'd like it if I could rearrange my uploads the way I want them, in MY order, not by most recent, author or anything else. I think it would be a great improvement, and kindly appreciated on my part."   ,
               "The Night reading mode is  bit overzealous -- the screen is bright orange at night! More generally:  Play Books is pretty nice. it is great to have a consistent x-platform experience.  But why doesnt Google take advantage of owning both Google Drive and Play Books? If I have a book in GD, and upload it to PB, I now have two copies. Each has their own separate annotations and bookmarks, not to mention taking up twice the storage.   This is particularly frustrating with books on the laptop. Here I have 2 reading options: Play Books's web app VS a real ebook reader sourcing the files from my Google Drive folder. Obviously I'll use the latter (SSD+SATA access speed vs web!). So now my annotations and bookmarks are out of sync between mobile and macbook.  Furthermore, none of the clients (iOS, Android, web) allow copying text, even with unrestricted PDFs. This is a bit nuts given this is one of only 3 advantages that electronic text has over the real thing (search, portability, copy/paste). How many people read non-fiction without copying sections for notes or review?"   ,
             " Now my favorite e-reader app Great clean design and is the best looking e-reader out there. Their upload feature for the cloud is amazing, which is the number one reason i am planning to stick with this app. Different book shelves or a way to categorize books is needed. Ability to make notes and view them as popups is one of my favorite features. I love the convenience of the widgets and how beautifully designed they are. Reading aloud has improved and I am amazed at how they are able to read my uploaded content as well. "   ,
               "Great app.  Less great policies. Storing notes and highlights on GDocs is an excellent idea.  it is easy to skim quickly through a book to find a section of interest or to get back to a section after a jump forward or back. Unfortunately G's policy on number of devices per book is very annoying.  There is a maximum of three devices per book, which seems a little tight but acceptable.  Except that it is very awkward to release a book from a device that isn't actually in your hand.  Your phone is suddenly defunct? Your tablet is at home?  Or you have more than three devices?  Yore out of luck, and cannot download the book to your device in hand."   ,
              "Difficult to find When I try to find the next in a series I have to jump through hoops then walk across a lake of fire to find  I would have thought it would be natural for the next edition to come up for grabs as a suggestion not a back issue that is 50 behind!!!!"   ,
             " The Edge of Never-Rated In Pain ( Because she rushed her relationship into having nowhere to go.....and then got high and drunk every day and treated him badly, missed work constantly, Ignored her children until they resented her, and finally collapsed into the arms of a weary man blinded by her beauty....All men would fall for this CUTIE.....but only ONE was stromg enough to keep her....He would try hard to escape by slowly turning his heart ice cold....Would the hero escape his fate by showing the maiden love.....or hate? A MUST READ!!"  ,
               "This Google app is installed on my phone and i never use it.  The only thing i can do is to turn the app off.  But it is still consumes memory on the internal storage for an app i never use.  dont want it.  Why is this app mandatory?  Junk for me."   ,
             " Looks great and works well, but limited audio book offerings/support. Google Books looks great and works well, with plenty of content available... Combined with a decent tablet - such as the waterproof Sony Xperia Z4 Tablet (the world's thinnest and lightest tablet!) - one has the perfect medium for eBooks and eComics. It is disappointing however, that so few commercial eBooks in the Google Play Store support the ability to have the eBook read out loud... A fact which causes two stars to lost - there simply is no excuse, with modern eBook technology and modern tablets."   ,
              "LOVE THIS APP!!!!!!!!!! I love to read!!!!! If u love reading, u will love this app!!! it is simple to use and downloads books fast....that's the beauty of it! The faster the download the faster I can start reading! Like I said best reading app ever!!!!! Wish there were more free series."   ,
               "If it is downloaded to my phone why do I have to use Internet to read and the read out loud is horrible voice You still have to use Internet to listen and down load horrible nt every one has unlimited data plan.dont have wifi not everyone has access to wifi. Stop making excuses other apps I have now found dont require wifi, or data to read a book aloud, or just read a book .plan and simple get with the program. If I could rate 0 I would since all you have are excuses and no improvements "  ,
             " I am Dedeepya So many interesting books r not free and many books we have to search in app store and if some books r free also we have to give card number and I am just a child. I am using my Daddy's account so I cannot give card number. Please give books without card number "  ,
             " cannot add my own books I remember why I never use this app now. I cannot add books that I have digital copies of. I have to buy them from the store." ,
             "To many fake profiles dont like that every other profile is fake,dont like that your personal preference doesnt matter in searching for people, & especially dont like that people use this to get money from people.", 
             "no use irritating app I have ever seen....... even though data connection is on... it is not connecting..... so, before downloading this app.. Read all the comments.....",
             "Just awful. Not enough filters unless you pay the monthly fee and when you do, the few extra filters you get dont work. Most people treat this app like a cross between Facebook and a hookup site. Really bad, would have given it negative stars if I could" ,
             "Load data long time and consume more network data in background Sometime cannot load data and app consume more network data in background",
             "Bad application It does not load the chat rooms and also cannot load the conversations so how I can use it .please tell me the soulation. It use my data but it is not working",
             "Fired up the app sucks I can never login and if I do it kicks me out the app just needs a lot of work it is way better and when you use it on the computer but nowadays people want to be able to use things on their phone I really wish they would fix this problem",
             "Pathetic, this is some truly poorly thought out code. Do you people even test these apps before releasing them to the public?",
             "Hate it now Keep getting System Error at login. I kept trying and it won't let me in. You guys need to fix your servers many are getting kicked off paltalk.",
             "Rubbish I thought it was my phone but after reading reviews its the new app that doesnt work didnt have this problem till i upgraded it and dont no about u others i find the login is worse if you use your mobile data connection instead of wifi connection constant log outs or disconnects you and room time outs paltalk need to sort this app and when you email them u get lame answers not solutions you cant log into it its hopeless paltalk solve the problems people are paying for this and weeks later still the same!",
             "Alex This update is missing a lot, for example. I can not even find out who is the entry and exit in the room and there is a problem in the audio Please rapid modification thank you",
             "Rubbish I thought it was my phone but after reading reviews its the new app that doesnt work didnt have this problem till i upgraded it and dont no about u others i find the login is worse if you use your mobile data connection instead of wifi connection constant log outs or disconnects you and room time outs paltalk need to sort this app and when you email them u get lame answers not solutions you cant log into it its hopeless paltalk solve the problems people are paying for this and weeks later still the same!",
             "Very poor I try alot of time to login on my andriod device but it doesnt work...",
             "Not good All i get is failed to join room due to timeout uninstalled it",
             "computer version SUCKS always disconnects.. popup ads and boxes, seems paltalk goes out of its way to be annoying.. while in the room you constantly get messages from paltalk warning about bootleg versions... yeah we read it the first time geez",
             "This is the worst app i have ever used.. dont even consider 1 star for this app... i wish i could rate it in negatives",
             "its not working so not happy Not working well",
             "Not that good anymore Used to be what the name may imply, but now it is just one big clusterf*ck of huge profiles playing around",
             "Dreadful UI Dreadful UI that is not intuitive. Periscope it has a much better user experience. Up periscope... as they say in the Navy.",
             "Unintuitive Terrible user interface, hard to use, frustrating to use, cannot use. Would give 0 stars if able",
             "Poor Support Have been trying to get support via Twitter to help me create an account in Bermuda. Two months later..........I wanted the app to watch U2 shows, now I've pretty much missed them all. Please contact me and help resolve my issue, I do not receive the SMS.",
             "Bugggs Said connection bad said connect lost then went into twitter and,watched it there u got bugs",
             "BAD DO NOT GET THIS APP IT DOSNT WORK IT WONT LET YOU POST IT ON ANY SOCIAL MEDIA OR SEND TO ANYONE AND THERE IS NO RE-DOWNLOAD BUTTON SO ONCE YOU DELETE THE PICTURE FROM YOUR MAIN CAMERA ROLE ITS GONE FOREVER DO NOT GET THIS APP IT IS GARBAGE",
             "Where's my files My phone rebooted but everything was the same in terms off my Gmail account but it deleted all my saved files in the folder so I wouldn't recommend it as u cannot recover the files",
             "Password Problem cannot open it.. Help me recover my files. I do not forgot my password. I need my files please help me.",
             "Good Good but not great. If you guys could put an ad blocker like to block pop ups on random website it would be awesome",
             "Stay away. I shouldn't even give it a star. It work for awhile but now its locked up my pin wont work and the photos are lost.",
             "Password not accepted!!!! Developer please help!!! Please!!! I installed this app coz of good reviews. I tried it and saved my precious photos on it and now it is not opening anymore. I know the password is correct. Please help me get my pictures back!!! Those are very precious to me coz it was my man who passed away last year. I need them please help me get them back.",
             "ERROR WHEN DIALING PASSWORD I cannot open this apps AGAIN!!! and i lost a lot of pics hide on this apps... Please fix this and bring my pics back!",
             "Why the hell i am not able to unhide my hidden pic Where ever i unhide it nothing happens and when ever i open this app a error msg comes that the file is too large",
             "WARNING!!! This. App. Steal pictures cannot unhide pictures every time I try says error. They keeping the people pictures. DONT INSTALL APP. WARNING. I UNINSTALLING. APP. Whoever is in charge of this app dont address nobody issues.",
             "doesnt open up my files again I dial my password but instead of opening like before, it calls instead. I once hid some important videos here but they didn't leave my gallery as they imported in the app. Fix it",
             "Very sad... Hd videos cannot hide I downloaded it to just hide HD video's but unfortunately it is impossible with using this app...!",
             "This app suck I have pictures on this app and now I cannot see none of them, it is just a black screen. Now I cannot see or get none of my pictures",
             "Stealth Mode Issue The basic code given isn't working anymore. I cannot see my photos cuz I cannot access the app. Am I gonna get an answer on this or no? Your app causes ppl to lose memories.",
             "Keep showing error It keeps showing connection time out. Error error error ergh!! I have reinstalled this app four times in a day but all in vain........ Total waste of efforts.......",
             "Error...... Always showed gateway error. UNINSTALLED",
             "Problem!! Will not let me use any email account. I have three email accounts and the app won't let me sign up with any of them. It keeps saying invalid email what gives?",
             "It sucks This app sucks dont bother downloafing it. Its just wasting your time it doesnt even work when you ask it questions, so no one bother downloading this app and wasting your time",
             "Lie detector I hated this app cause I had a 50$ and if I lied I would have to give the money up so my BFF told me to put my hand on the lie detector so I did a I said I am the best at call of duty and I am so I put my hand on the lie detector and it said lie that is why I hate it sooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo much. Now let's play a game loooooooooooooooooo9oooooooooooooooooooooooooooooooooooooooooooo try to find the 9.",
             "Horrible Horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible it. dont work horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible horrible it dont work",
             "Hate it it is stupid it keeps doing lie and that is true Hate hate hate hate hate stupid stupid stupid stupid",
             "Horrible I hate it! Never ever get it! I would never recommend it to anyone! dont waste your storage!",
             "I Hate this stupid APP How do u even hear our voice in a different way? OH I KNOW! U CANT! There are too many stupid adds I went on it today and at least 20 popped up and as soon as I got rid of them they popped up again so if our thinking of downloading this stupid app dont u will be dissapointed will give it a few more chances it wont work so u will hate it! And its a real pile of stupidity poo I HATE IT!",
             "I HATE THIS APP SO SO MUCH!!!!! Everytime i select a voice thing, A STUPID AD COMES UP AND IF I DONT CLICK ON THE AD OR ANYWHERE ELSE,IT WILL MAKE ME GO INSTALL ANOTHER STUPID APP!!!!!!!!! I HATE THIS DONT GET IT PPL!",
             "HATE IT!!! NEVER GET THIS APP So annoying. Too many annoying adds that pop up without an x button. Plus hurts my ears by bursting noise. I would give this no stars if it were possible. Worst app ever.",
             "I RATE 0 STARS. IT ALL SOUNDS THE SAME. CANT HEAR YOURSELF, TOO MANY ADDS! DO NOT WASTE YOUR STORAGE, PEOPLE! IM JUST A KID TOO.",
             "Crappy Too many ads and u cannot even hear your self so crapp",
             "it is dumb I hate this app what's the deal of doing this this stupit app is f*** horrible"]

# compile sample documents into a list
#doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e,doc_f,doc_g,doc_h,doc_i]
doc_set = documents

# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_set:
    
    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]
    
    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    
    # add tokens to list
    texts.append(stemmed_tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)
    
# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]


# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=35, id2word = dictionary, passes=20)
#ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word = dictionary, passes=20)

#print(ldamodel.print_topics(num_topics=3, num_words=3))
print(ldamodel.print_topics(num_topics=35, num_words=20))