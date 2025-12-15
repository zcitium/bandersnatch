print("bandersnatch")

while True:
    print("pick a cereal")
    cereal = input("enter the option : \n a) kellogs frosties \n b) quaker suger puffs \n")
    if cereal == 'a':
        print("take bus to tuckersoft")
        break
    if cereal == 'b':
        print("take bus to tuckersoft")
        break

while True:
    print("pick music")
    music = input("enter the option : \n a) now thats what i call music \n b) thompson twins \n")
    if music == 'a':
        print("here comes the rain by eurythmics plays during commute")
        break
    if music == 'b':
        print("hold me now by thompson twins plays during commute")
        break

while True:
    print("meet mohan, tucker and colin. get offer to make bandersnatch at tuckersoft")
    offer = input("enter the option : \n a) accept \n b) refuse \n")
    if offer == 'a':
        print("bandersnatch is a rushed job. Gets 0/5 stars from robin (reviewer)")
        print("dead end")
        print("try again")

    if offer == 'b':
        break

while True:
    print("go to therapists office...Talk about mom?")
    mom = input("enter y for yes and n for no")
    if mom == 'n':
        print("therapist asks again")
        mom = input("enter y for yes and n for no")
        if mom == 'n':
            break
    if mom == 'y':  #why is it working
        print("childhood trauma")
        print("refused to go with mom")
        print("mom dies")
        break

while True:
    print("go to the record store.. which vinyl")
    vinyl = input("enter your option \n a) The bermuda triangle \n b)phaedra ")
    if vinyl == 'a':
        print("game dev montage with bermuda triangle in the background")
        break
    if vinyl == 'b':
        print("game dev montage with phaedra in the background")
        break

while True:
    print("dad asks about lunch. Stefan gets angry... whats the reaction?")
    reaction = input("enter your option \n a) Throw tea over computer \n b)shout at dad \n")
    if reaction == 'a':
        print("dead end \n try again")
    if reaction == 'b':
        break

print("taken to therapist by dad")

while True:
    print("stefan sees colin passing by")
    colin = ' '
    follow = input("enter your option \n a) see dr haynes  \n b)follow colin \n")
    if follow == 'b':
        colin = 'y' #have to check if he ever went to colin

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

print("delivery day but stefan needs more time")
while True:
    if jump == 'b':
        print("colin is AWOL")
        print("an intern hands stefan a tape and says its from colin")
    print("colin gives stefan a documentary about davies")
    if cereal == 'a':
        print("kellogs frosties ad plays")
        break
    if cereal == 'b':
        print("quaker suger puffs ad plays")
        break