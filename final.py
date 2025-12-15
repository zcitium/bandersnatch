print("bandersnatch")
global cereal, music, offer, mom, vinyl, reaction, jump, colin, follow, lsd, frustrated
global item, passwd, mom2, visit, pills, pacs, frust, photo, kd, react1, exit1, dad1, dad, pearl, react2
global mohan, option, action, act, ques2, ques, more, number, bkd


def A():
    while True:
        global cereal
        print("pick a cereal")
        cereal = input("enter the option : \n a) kellogs frosties \n b) quaker suger puffs \n")
        if cereal == 'a':
            print("take bus to tuckersoft")
            break
        if cereal == 'b':
            print("take bus to tuckersoft")
            break


A()


def B():
    while True:
        global music
        print("pick music")
        music = input("enter the option : \n a) now thats what i call music \n b) thompson twins \n")
        if music == 'a':
            print("here comes the rain by eurythmics plays during commute")
            break
        if music == 'b':
            print("hold me now by thompson twins plays during commute")
            break


B()


def C():
    while True:
        global offer
        print("meet mohan, tucker and colin. get offer to make bandersnatch at tuckersoft")
        offer = input("enter the option : \n a) accept \n b) refuse \n")
        if offer == 'a':
            print("bandersnatch is a rushed job. Gets 0/5 stars from robin (reviewer)")
            print("dead end")
            print("try again")

        if offer == 'b':
            break


C()


def D():
    while True:
        global mom
        print("go to therapists office...Talk about mom?")
        mom = input("enter y for yes and n for no")
        if mom == 'n':
            print("therapist asks again")
            mom = input("enter y for yes and n for no")
            if mom == 'n':
                break
        if mom == 'y':  # why is it working
            print("childhood trauma")
            print("refused to go with mom")
            print("mom dies")
            break


D()


def E():
    while True:
        global vinyl
        print("go to the record store.. which vinyl")
        vinyl = input("enter your option \n a) The bermuda triangle \n b)phaedra ")
        if vinyl == 'a':
            print("game dev montage with bermuda triangle in the background")
            break
        if vinyl == 'b':
            print("game dev montage with phaedra in the background")
            break


E()


def F():
    global reaction
    while True:
        print("dad asks about lunch. Stefan gets angry... whats the reaction?")
        reaction = input("enter your option \n a) Throw tea over computer \n b)shout at dad \n")
        if reaction == 'a':
            print("dead end \n try again")
        if reaction == 'b':
            break


F()


def G():
    global follow, colin, jump, visit, lsd, pills
    print("taken to therapist by dad")
    jump = ' '
    while True:
        print("stefan sees colin passing by")
        follow = input("enter your option \n a) see dr haynes  \n b)follow colin \n")
        colin = ' '
        if follow == 'b':
            colin = 'y'  # have to check if he ever went to colin

            while True:
                print("take lsd?")
                lsd = input("enter y for yes and n for no")
                if lsd == 'n':
                    print("colin spikes tea")
                print("stefan is high and listening to colins theories")
                break
            while True:
                print("colin asks who jumps from the balcony")
                jump = input("enter your option \n a) stefan \n b)colin \n")
                if jump == 'a':
                    print("stefan is dead \n bandersnatch finished abruptly")
                    print("dead end \n try again")
                if jump == 'b':
                    print("stefan wakes up as if from a nightmare")
                    break

        if follow == 'a':
            visit = input("enter your option \n a)bite nails  \n b)pull earlobe \n")
            print("prescription dosage increased \n do you take your pills?")
            if colin == 'y':
                pills = input("enter your option \n a)throw pills in trash  \n b)flush pills \n")
                break
            colin = 'n'
            if colin == 'n':
                pills = input("enter your option \n a)flush pills  \n b)take pills \n")
                if pills == 'b':
                    print("bandersnatch releases and gets 2.5/5 stars")
                    print("dead end \n try again")
                if pills == 'a':
                    break
            break


G()
print("delivery day but stefan needs more time")

if jump == 'b':
    print("colin is AWOL")
    print("an intern hands stefan a tape and says its from colin")
    print("colin gives stefan a documentary about davies")
if cereal == 'a':
    print("kellogs frosties ad plays")
if cereal == 'b':
    print("quaker suger puffs ad plays")

print("Documentary plays")
print("Stefan gets frustrated ")


def H():
    global frustrated, item, mom,photo
    while True:
        frustrated = input("enter the option : \n a) Hit desk \n b) Destroy computer ")
        if frustrated == 'b':
            print("Dead end \n try again")
            # Documentry walla goto
            break
        if frustrated == 'a':
            print("Select item to take to bed . ")
            item = input("enter the option : \n a) Book \n b) Family Photo ")
            if item == 'b':
                print("Stefan goes to the bathroom mirror ")
                photo = 'y'
                if mom == 'n':
                    print("the mirror breaks ")
                    print("Stefan wakes up (as if from a nightmare ) ")
                    break
                elif mom == 'y':
                    print("He goes through the mirror into his childhood ")
                    print("Stefan wakes up (as if from a nightmare ) ")
                    break
            if item == 'a':
                print("Stefan will access his dad's safe ")
                photo = 'n'
                break


H()


def I():
    global passwd, pacs,photo, bkd
    pacs = ' '
    # password
    while True:
        if colin == 'n':
            passwd = input("enter your option \n a)PAX \n b)JFD \n")
            if passwd == 'a':
                print("pax the monster from bandersnatch lunges towards stefan")
                print("stefan wakes up as if from a nightmare")
                pacs = 'n'
                break
            if passwd == 'b':
                print("Jerome F Davies appears and laughs maniacally")
                print("stefan wakes up as if from a nightmare")
                pacs = 'y'
                break
        if colin == 'y':
            passwd = input("enter your option \n a)PAX \n b)PACS \n")
            if passwd == 'a':
                print("pax the monster from bandersnatch lunges towards stefan")
                print("stefan wakes up as if from a nightmare")
                break
            if passwd == 'b':
                print("stefan unearths a disturbing conspiracy")
                print("stefan wakes up as if from a nightmare")

                break

        if colin == 'y' and mom == 'y' and photo == 'y' and kd == 'y':
            passwd = input("enter your option \n a)PAX \n b)TOY \n")
            if passwd == 'a':
                print("pax the monster from bandersnatch lunges towards stefan")
                print("stefan wakes up as if from a nightmare")
                break
            if passwd == 'b':
                print("stefan is 5 again \n he finds the rabbit")
                while True:
                    print("stefans mom invites him to board the late train")
                    mom2 = input("enter y for yes and n for no")
                    if mom2 == 'y':
                        print("cut to modern day. \n stefan is dead in his chair during the first therapy session")
                        print("YOU REACHED DEATH ENDING")
                        exit()


I()


def who_shows_up():
    global react1, react2, exit1
    if colin == 'y':
        print("kitty asks if stefan knows where colin is")
        react1 = input("How do you wanna react a) No idea  b) He jumped ")
        if react1 == "a":
            print("Kitty tells Stefan to call her if he sees him")
            print("The dog digs up Stefan's dad's body later that night ")
            print("Jail ending")
            exit()
        elif react1 == "b":
            print("Kitty claims that never happened ")
            print("Kitty tells Stefan to call her if he sees him")
            print("The dog digs up Stefan's dad's body later that night ")
            print("Jail ending")
            exit()
    if colin == 'n':
        print("colin asks if Stefan is going to kill him too?")
        react2 = input("How do you wanna react a) Yes  b) No ")
        if react1 == "a":
            print("Stefan kills Colin ")  # both these ending lead to end
        elif react1 == "b":
            print("Colin leaves  ")
            exit1 = input(
                "this is an official ending do you want to a) exit b) go back to a previous scenario")  # go back upar
            if exit1 == 'a':
                print("jail ending")
                exit()


def symbol():
    global dad, pearl, mohan, dad1,bkd
    print("Stefan feels out of control ")
    dad = input(" How do you want to react a) Backoff \n  b) Kill Dad  \n ")
    if dad == 'a':
        I()
        bkd = 'y'
    elif dad == 'b':
        dad1 = input("Stefan asks what should he do a) Bury him \n b) Chop up his body ")
        if dad1 == 'b':
            print("Stefan sets up an appointment "
                  "with his therapist for tomorrow.\n Mohan tucker calls but the line is busy . ")
            print("Stefan finishes his game. He talks to his therapist about it .")
            print("Stefan's secret is uncovered , he goes to jail and Bandersnatch "
                  "is pulled from shelves due to controversy despite 5/5 Star rating. ")
            print("modern era. Colins daughter Pearl decides to do a remake of"
                  " Bandersnatch for a streaming platform Rumoured to be Netflix .")
            pearl = input("Pearl gets frustrated while coding \n. "
                          "How do you want to react a)Throw tea over computer \n b)Destroy computer ")
            if pearl == 'b':
                print("Screen gets black")
            elif pearl == 'a':
                print("This is an official ending \n. How do you want to proceed a)Exit to credits \n b) continue \n")
                print("go back to scenario ")  # go to statement needed
            print('"History repeats itself" Ending ')
            exit() # flow ngi samja

    elif dad1 == 'a':
        mohan = 0
        mohan += 1
        print("Mohan Tucker calls and asks if the game can be done by today ")
        if mohan == 1:
            game = input("How do you wanna react a) Yes b) No")
            who_shows_up()
        if mohan == 2:
            print("stefan responds without actually hearing tucker ask the question")
            who_shows_up()
        if mohan == 3:
            print("stefan hangs up without hearing the question")
            print("stefan murders mohan tucker too \n jail ending")
            exit()


def J():
    print("Stefan gets frustrated again with game dev")
    global frust, option, more, ques, ques2, action, act, number
    while True:
        frust = input(" How do you want to react a) Destroy computer \n  b) Throw tea over computer \n ")
        print("Stefan refuses and asks 'Who's there ?")
        if pacs == 'n':
            option = input("enter your option \n a)Symbol  \n b)netflix \n")
            if option == 'a':
                symbol()
            if option == 'b':
                print("netflix?")
                more = input("enter your option \n a)Tell him more  \n b)Try to explain \n")
                print("stefan has more questions")
                ques = input("enter your option \n a)Tell him more  \n b)Stop the conversation \n")
                print("Dad walks in, stefan is taken to see Dr Haynes")
                print("Dr Haynes questions this logic.Wouldn't you want a little more action"
                      " if you were watching this now on teli?")
                ques2 = input("enter your option \n a)yes  \n b)yes \n")
                print("fight scene breaks out")
                print("Stefan throws coffee in her face and she wields 2 batons. leap through the window or fight her?")
                action = input("enter your option \n a)leap through the window  \n b)fight her \n")
                if action == 'a':
                    print("director yells cut! Stefan is actually just on set")
                    print("this is an official ending. Exit to credits or continue")
                    break

                if action == 'b':
                    print("Dad appears.Karate chop dad or kick him in the balls?")
                    act = input("enter your option \n a)Karate chop dad \n b)kick him in the balls \n")
                    print("Stefan is dragged out yelling about netflix")
                    print("this is an official ending. Exit to credits or continue")
                    break

            if pacs == 'y':
                option = input("enter your option \n a)Symbol  \n b)PACS \n")
                if option == 'a':
                    symbol()
                if option == 'b':
                    print("PACS")
                    print("Stefan kills dad")
                    print("Stefan dials Dr Haynes. Will you input the number correctly?")
                    number = input("enter your option \n a)20541 \n b)incorrect number \n")
                    if number == 'a':
                        print("Stefan calls up Dr Haynes office and threatens "
                              "to kill Dr Haynes just like he killed his dad")
                        print("Stefan buries dad")
                        print("sirens flash in background")
                        print("stefan is in jail")
                        print("this is an official ending. Exit to credits or continue")
                        exit()
                    if number == 'b':
                        print("Number you dialled is incorrect,call doesn't go through")
                        print("stefan buries dad")
                        print("stefan's dog digs up dad later that night")
                        print("stefan is in jail")
                        exit()



J()
