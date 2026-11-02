
"""
Mini search engine built with a Trie and a Heap.

Reads all .txt files from the 'datafiles' folder next to this script.
Assumption: the files contain only letters, numbers, spaces and full stops.
Other characters are treated as word separators.
"""


from pathlib import Path
import heapq as h



class TrieNode :
    '''
    This creates a normal node, but it includes an information variable 
    which is necessary for the search engine I built.
    '''
    def __init__(self) :
        self.children = {}
        self.is_end = False
        self.information = {}


class TopWordsFinder :
    """
    Find the 5 most used words that start with a given prefix.
    Words are ranked by their total count across all files.
    """
    def __init__(self,prefix,is_word,node) :
        '''
        This constructor defines a stack and a heap, and runs a recursive 
        function so that the heap ends up giving the exact final result.
        '''
        self.node = node
        self.stack_result = []
        self.heap = []
        if prefix is not None :
            for j in prefix :
                self.stack_result.append(j)
        if is_word is True :
            self.__heap_update(node,prefix)
        self.collect_words(self.node)

    def __heap_update(self,lastnode,newword) :
        '''
        Sum up how many times a word appears across all data, 
        pushes them into the heap, and if the heap length exceeds 5, 
        it pops the smallest appear word.
        '''
        tempsum = 0
        for i in lastnode.information :
            tempsum += lastnode.information[i]
        h.heappush(self.heap,(tempsum,newword))
        if len(self.heap) > 5 :
            h.heappop(self.heap)

    def collect_words(self,node) : 
        '''
        The prefix's last node goes into its input, then pushes all words formed 
        beneath it into the heap while continuously updating the heap so that 
        in the end, we get exactly the top 5 words in the heap.
        '''             
        for i in node.children :
            nextnode = node.children[i]
            if nextnode.is_end == True :
                self.stack_result.append(i)
                newstr = "".join(self.stack_result)
                self.__heap_update(nextnode,newstr)
            else :
                self.stack_result.append(i)
            self.collect_words(nextnode)
        if len(self.stack_result) > 0 :
            self.stack_result.pop()

    def get_topwords(self) :
        '''
        This will sort the heap present in the constructor in descending order 
        since the heap is already built, and then simply returns that heap.
        '''
        maximum = sorted(self.heap,reverse=True)
        return maximum



class TrieBuilder :
    """
    This class does not take inputs. According to the logic defined in the code, 
    wherever the file is run, there will be a 'datafiles' folder containing the data files. 
    Treating those as data, it builds a trie structure.
    """
    def __init__(self) :
        self.path = self.__find_data_folder()
        self.root = TrieNode()

    def __find_data_folder(self) :
        '''
        Wherever the user's code file is located, it finds that path and connects 
        to the 'datafiles' folder. If the folder exists, that path is returned; 
        otherwise, it returns false indicating an error in data extraction 
        and the process stops.
        '''
        curr_folder = Path(__file__).resolve().parent
        datafolder = curr_folder / "datafiles"
        if datafolder.exists() is False :
            return False
        return datafolder

    def __add_word(self,userword) :
        '''
        This adds the word to the trie in a standard way.
        '''
        curr = self.root
        index = 0
        while index != len(userword) :
            char = userword[index]
            if char not in curr.children :
                newnode = TrieNode()
                curr.children[char] = newnode
                curr = newnode
            else :
                curr = curr.children[char]
            index += 1
        curr.is_end = True
        return curr

    def __adjust_information(self,lastnode,filename) :
        '''
        This is used when a word is added to the trie; we update the last node's 
        information variable. If it's a new file, we add a new file to its information dictionary, 
        and if it already exists, we add 1 to its word count.
        '''
        if filename in lastnode.information :
            lastnode.information[filename] += 1
        else :
            lastnode.information[filename] = 1


    def __extract_words(self,userstring,filename) :
        '''
        This extracts words from the entire string and simultaneously adds them to the trie. 
        The word extraction logic is written in the readme and will also be clear from the code.
        '''
        stack = []
        for i in userstring :
            if i.lower() in "abcdefghijklmnopqrstuvwxyz" or i in "0123456789" :
                stack.append(i.lower())
            else :
                if stack == [] :
                    continue
                newstr = "".join(stack)
                lastnode = self.__add_word(newstr)
                self.__adjust_information(lastnode,filename)
                stack = []
        if stack != [] :
            newstr2 = "".join(stack)
            lastnode2 = self.__add_word(newstr2)
            self.__adjust_information(lastnode2,filename)

    def __get_filenames_strings(self) :
        '''
        This function loads all `.txt` files present in `self.path` into a string, 
        and then passes it to the `__extract_word(string, filename)` function to extract words 
        and add them to the trie, handling further steps automatically.
        '''
        for i in self.path.iterdir() :
            if i.is_file() and i.suffix == ".txt" :
                with open(i,"r",encoding="utf-8") as file :
                    string = file.read()
                    self.__extract_words(string,i.name)

    def gettrie(self) :
        '''
        This is the main function of this class. If `self.path` exists, it runs 
        the `__get_filesname_string()` function, saving all data into a trie. 
        If the path is invalid, it returns None and no trie is built.
        '''
        if self.path is False :
            return None
        self.__get_filenames_strings()
        if len(self.root.children) == 0 :
            return None
        return self.root

class SearchEngine :
    """
    This class will perform searching functions on the trie you provided.
    """
    def __init__(self,userroot) :
        self.root = userroot

    def __search_word_prefix(self,userword) :
        '''
        Checking the existence of words and prefixes, and accessing their last node, 
        both tasks use the same logic. Therefore, this function is designed to be 
        useful for both and returns three things: 
        First, false if the word or prefix does not exist in entire data; 
        Second, true/false whether the prefix exists in the data; 
        Third, if the last node exists, it returns it, otherwise None.
        '''
        curr = self.root
        index = 0
        while index != len(userword) :
            char = userword[index]
            if char not in curr.children :
                return False,False,None
            curr = curr.children[char]
            index += 1
        if curr.is_end == False :
            return False,True,curr
        return True,True,curr

    def search_word(self,userword) :
        '''
        Searches for the user-given word in the data, first stripping leading 
        and trailing blank spaces and converting it to lowercase since the data is stored in lowercase. 
        Returns 2 things: first, the status of whether the complete word was found, and second, its information.
        '''
        word = userword.strip().lower()
        wstatus,pstatus,lastnode = self.__search_word_prefix(word)
        if wstatus is False :
            return wstatus,None
        return wstatus,lastnode.information


    def top5_files(self,userword) :
        '''
        A word can appear in multiple files within the data. 
        This function shows the user only the top 5 files where the words appeared the most.
        '''
        word = userword.strip().lower()
        status,info = self.search_word(word)
        if status is False :
            return False
        heap = []
        for i in info :
            val = (info[i],i)
            h.heappush(heap,val)
            if len(heap) > 5 :
                h.heappop(heap)
        heap.sort(reverse=True)
        return heap

    def top5_words(self,userprefix) :
        '''
        The prefix entered by the user can have beneath multiple words. 
        This function will display only the top 5 words, which are those 
        that appear most frequently in the data starting with that prefix.
        '''
        prefix = userprefix.strip().lower()
        wstatus,pstatus,lastnode = self.__search_word_prefix(prefix)
        if lastnode is None :
            return False
        else :
            mainlist = TopWordsFinder(prefix,wstatus,lastnode).get_topwords()
            return mainlist


'''
All logic is complete; the code below is written to create terminal commands.
'''

def welcome() :
    '''for print welcome and introduction lines '''
    print("="*50)
    print("WECOME TO VERY SMALL SEARCH ENGINE")
    print("YOU CAN PERFORM DIFFERENT SEARCH FUNCTIONS ON THIS PROGAME")
    print("="*50)

def choices() :
    '''Show users applications of the code '''
    print("\n")
    print("-"*50)
    print("1.ENTER A WORD AND SEE IS EXISTED IN DATA AND SEE ITS PRESENCE IN TOP 5 FILES")
    print("2.ENTER A PREFIX  AND SEE THE TOP 5 WORDS MATCHING IN ENTIRE DATA")
    print("3.TO EXIT PROGRAME")
    print("ENTER NUMBERS AS OPTION")
    print("-"*50)
    print("\n")


def run_programe() :
    '''this se main function in which all code class and its fucntion are used 
    and its runs for terinal for user
    '''
    mytrie = TrieBuilder().gettrie()
    if mytrie is None :
        print("THE DATA FOLDER HAS BEEN TAMPERED WITH, DATA CANNOT BE ACCESSED--------------")
        print("PLEASE RE-DOWNLOAD THE CODE AND DO NOT ALTER THE 'DATAFILES' FOLDER AGAIN")
        print("\n")
        return
    search = SearchEngine(mytrie)
    welcome()
    choices()
    while True :
        userinput = input("ENTER YOUR OPTIONS  :  ")
        if userinput == "1" :
            userword = input("ENTER YOUR WORD  :  ")
            result = search.top5_files(userword)
            if result is False :
                print(f"'{userword}' THIS WORD DOES NOT EXIST IN THE DATA")
            else :
                print("#"*30)
                for i in result :
                    print(f"FILENAME : '{i[1]}'  ,, PRESENECE COUNT : {i[0]} ")
                print("#"*30)

        elif userinput == "2" :
            userprefix = input("ENTER PREFIX  :  ")
            result = search.top5_words(userprefix)
            if result is False :
                print(f"'{userprefix}' THIS PREFIX DOES NOT EXIST IN THE DATA")
            else :
                print("#"*30)
                for j in result :
                    print(f"WORD  :  {j[1]}  ,, WORD REPEATS  {j[0]} TIMES")
                print("#"*30)
        elif userinput == "3" :
            print("-----------------------GOOD BYE-------------------------")
            print("----------------------------------------------")
            break

        else :
            print("YOU ONLY CHOOSE OPTIONS FROM (1-3)")
        print("\n")

if __name__ == "__main__":
    run_programe()

