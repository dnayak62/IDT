import string
import nltk
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
class FunctionalRequirement:
    def __init__(self, name,dependencies=None):
        self.name = name
        self.dependencies = dependencies or []

class DesignParameter:
    def __init__(self, name,dependencies=None):
        self.name = name
        self.dependencies = dependencies or []

def analytical_proposition(text):
    # Tokenize the input sentence into words
    words = word_tokenize(text)

    # Perform part-of-speech tagging on the words
    tagged_words = pos_tag(words)

    # Find the first noun and verb in the tagged words
    noun = ""
    verb = ""
    for word, tag in tagged_words:
        if tag.startswith('N'):
            noun = word
        elif tag.startswith('V'):
            verb = nltk.stem.WordNetLemmatizer().lemmatize(word, pos='v')

    # Generate a logical proposition using the noun and verb
    if noun != "" and verb != "":
        proposition = f"To {verb} {noun}."  
        return proposition
    else:
        return "Unable to generate a proposition."
    
def FR():
    flag = True
    sentence = input("Enter a NEW SUB FR or 'n' to quit: ")
    if sentence == 'n':
        return False
    prop = analytical_proposition(sentence)
    print("You entered: ", prop)
    choice = input("Is the FR complete, simple ?(Enter 0 for yes, 1 for no): ")
    while choice not in ['0', '1'] and flag:
        choice = input("Invalid input. Please enter 0 if you're satisfied with the SUB FR, or 1 if you'd like to enter a new SUB FR ")
        if choice == '1':
            flag = False
            break

    while choice == '1' and flag:
        sentence = input("Please enter a MODIFIED SUB FR")
        prop = analytical_proposition(sentence)
        print("You entered: ", prop)
        modify_choice = input("Do you want to modify this MODIFIED SUB FR? (Enter 0 for yes, 1 for no): ")
        if modify_choice == '1':
            flag = False
            break

        while modify_choice not in ['0', '1'] and flag:
            modify_choice = input("Invalid input. Please enter 0 if you want to modify this MODIFY NEW SUB FR, or 1 if you're satisfied with this MODIFIED SUB FR: ")
            if modify_choice == '0':
                continue
            else:
                flag = False

    return prop

def create_FR():
    i = 1
    hm = dict()
    flag = True
    while flag:
        if flag:
         prop = FR()
         hm[f"FR{i}"] = FunctionalRequirement(prop)
         i += 1
        else:
         flag = False
        stop_choice = input("Enter 'n' to stop or any other key to continue: ")
        if stop_choice == 'n':
            flag=False
    return hm

def partof(layer1, Frmain):
        flag = True
        i=1
        while flag and i <= len(layer1):
            j = input(f"{layer1[f'FR{i}'].name} is a part of {Frmain.name} (y/n): ")
            if j.lower() == 'y':
                i+=1
            else:
                flag = False
                return i
        return 0

def specifiedby(layer1,Frmain):
        flag = True
        i=1
        while flag and i <= len(layer1):
            j = input(f"{Frmain.name} is specified by {layer1[f'FR{i}'].name} (y/n): ")
            if j.lower() == 'y':
                i+=1
            else:
                flag = False
                return i
        return 0

def check_independence(hm):
    values = [fr.name for fr in hm.values()]
    print("Values:", values)  # Print the values list
    choice = input(f"Are all objects in values independent? (y/n): ")
    if choice=='y' and flag:
        flag=1
    else:
        change=input(f"which FR is wrong ? ")
        text=input(f"Enter new FR: ")
        newFR= analytical_proposition(text)
        hm[f"FR{change}"].name = newFR

def synthetic_proposition(text):
    # Tokenize the input sentence into words
    words = word_tokenize(text)

    # Perform part-of-speech tagging on the words
    tagged_words = pos_tag(words)

    # Find the first noun and verb in the tagged words
    noun = ""
    verb = ""
    for word, tag in tagged_words:
        if tag.startswith('N'):
            noun = word
        elif tag.startswith('V'):
            verb = nltk.stem.WordNetLemmatizer().lemmatize(word, pos='v')

    # Generate a phrase using the noun and verb
    if noun != "" and verb != "":
        phrase = f"{noun}."
        return phrase
    else:
        return "Unable to generate a phrase."

def DP(i):
    prop = None
    flag=True
    while flag:
        sentence = input(f"Enter a NEW SUB DP for FR{i} ('n' to quit): ")
        if sentence == 'n':
            break
        prop = synthetic_proposition(sentence)
        print("You entered:", prop)
        choice = input("Does the DP satisfy the external constraints? (Enter 0 for yes, 1 for no): ")
        if choice == '0' and flag:
            flag=False
            return prop
    return None

    


def create_subDPs(i):
    j='a'
    hm = dict()
    flag = True
    while flag and j in string.ascii_lowercase:
        prop = DP(i)
        hm[f"DP{i}{j}"] = DesignParameter(prop)
        j = chr(ord(j) + 1)
        choice = input(f"Do you want to enter more possible design parameters for FR{i}? (Enter y for yes or n for no)")
        if choice == 'n':
            flag = False
    return hm

def optionspacefiles(layer1, hm, a):
    ch = 'a'
    for i in range(1, 3):
                dp_key1 = f"DP{i}{ch}"
                for j in range (1,3):
                 dp_key2 = f"DP{2}{ch}"
                 ch = chr(ord(ch) + 1)
                 filename = f"optionspace{j}"
                 with open(filename, 'w') as f:
                  for key, value in layer1.items():
                   f.write(f"{key}: {value.name}\n")
                   f.write(f"{dp_key1}: {hm[dp_key1].name}\n")
                   f.write(f"{dp_key2}: {hm[dp_key2].name}\n")
                 


                 
           

                    



def createDPs(layer1):
    hm = {}
    a=[]
    for i in range(1, len(layer1) + 1):
        print(f"Enter DP for FR{i} or 'n' to stop")
        layer2 = create_subDPs(i)
        hm.update(layer2)
        a.append(len(layer2))
    return hm, a

    



    







def main():
    text = input("Enter a Main FR: ")
    Frmain= FunctionalRequirement(text)
    layer1={}
    layer1=create_FR()
    hm={}
    a=[]
    
    

    check_independence(layer1)
    hm, a =createDPs(layer1)
    print(hm["DP1a"].name)
    print(hm["DP1b"].name)
    optionspacefiles(layer1, hm, a)
    
    

    
    # Ask the user if they want to check if layer1 is part of Frmain
    check_partof = input("Do you want to check if layer1 is part of Frmain? (y/n): ")
    flag=True
    if check_partof.lower() == 'y' and flag:
        partofcheck= partof(layer1,Frmain)
        if partofcheck != 0 and flag:
            newsubFR= FunctionalRequirement(FR())
            layer1[f'FR{partofcheck}'] = newsubFR
        else:
            flag=False
    else:
        flag= False
    
    check_specifiedby = input("Do you want to check if Frmain is specified by layer1? (y/n): ")
    flag=True
    if check_specifiedby.lower() == 'y' and flag:
        specifiedbycheck=specifiedby(layer1,Frmain)
        if specifiedbycheck != 0 and flag:
            newsubFR= FunctionalRequirement(FR())
            layer1[f'FR{specifiedbycheck}']= newsubFR
        else:
            flag=False
    else:
        flag=False
    
    

 

        

    

if __name__ == "__main__":
    main()