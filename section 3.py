while True:
    if pacs == 'n':
        print("netflix?")
        more = input("enter your option \n a)Tell him more  \n b)Try to explain \n")
        print("stefan has more questions")
        ques = input("enter your option \n a)Tell him more  \n b)Stop the conversation \n")
        print("Dad walks in, stefan is taken to see Dr Haynes")
        print("Dr Haynes questions this logic.",end=' ')
        print("Wouldn't you want a little more action if you were watching this now on teli?")
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
        print("PACS")
        print("Stefan kills dad")
        print("Stefan dials Dr Haynes. Will you input the number correctly?")
        number = input("enter your option \n a)20541 \n b)incorrect number \n")
        if number == 'a':
            print("Stefan calls up Dr Haynes office and threatens to kill Dr Haynes just like he killed his dad")
            print("Stefan buries dad")
            print("sirens flash in background")
            print("stefan is in jail")
            print("this is an official ending. Exit to credits or continue")
        if number == 'b':
            print("Number you dialled is incorrect,call doesn't go through")
            print("stefan buries dad")