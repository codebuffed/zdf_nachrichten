import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import soups
import doublyLinkedListSource as dll
import textwrap

def format_article(s, width):
    result = textwrap.fill(s, width=width, break_long_words=True)+2*'\n'
    return result

#actual article
def articleWindow(article_link):
    if soups.article(article_link):
        # create new window and it's geometry
        article_window = tk.Toplevel(topic)
        article_window.geometry('900x1000')

        # call soups.article method with article_link as argument -> returns a tuple ({'author':'albert einstein', ...}, [paragraph1, paragraph2, paragraph3, ...])
        content = soups.article(article_link)


        titles = content[0]['titles']

        #traverse doubly_ll until node start
        node = doubly_ll.traverse_list(article_link)

        ## initialize the widgets with 'clicked' article from newWindow
        label_title = tk.Label(article_window, text='\n'.join(titles), underline=True, font=('Helvetica',20))
        label_title.grid(row=0, column=0)

        text = tk.Text(article_window, width=20, height=30, font=('helvetica',18))
        text.grid(row=1,column=0, sticky='nsew')

        button_frame = tk.Frame(article_window, height=5, width=40)
        button_frame.grid(row=2, column=0)

        # the 'text content' of the article is stored in the second element of a tuple from soups.article as a list
        for p in content[1]:
             text.insert(tk.END, format_article(p, 40))


        for key, val in content[0].items():
            if key != 'titles' and val:
                text.insert(tk.END, str(key)+' : '+str(val)+'\n')


        # check if article child node exists //
        # if node.prev == None -> Beginning of list -> disable prev_button || vice versa for the end of the  list
        if node.prev:
            prev_button = tk.Button(button_frame, text='<<',
                                    command=lambda: change_article(False),
                                    state=tk.NORMAL,
                                    pady=40,
                                    padx=40,
                                    bg='green',
                                    )
            prev_button.grid(row=0, column=0)
        else:
            prev_button = tk.Button(button_frame, text='<<',
                                    state=tk.DISABLED,
                                    pady=40,
                                    padx=40,
                                    bg='green',
                                    )

            prev_button.grid(row=0, column=0)

        quit_button = tk.Button(button_frame,text='Quit',
                                command = article_window.destroy,
                                bg = 'red',
                                )
        # quit_button.pack(button_frame,side ='top', pady=40, padx=40)
        quit_button.grid(row=0, column=1, pady=40, padx=40)

        if node.next:
            next_button = tk.Button(button_frame, text='>>',
                                    command=lambda: change_article(True),
                                    state=tk.NORMAL,
                                    pady=40,
                                    padx=40,
                                    bg = 'green',
                                    )
            next_button.grid(row=0, column=2,)
        else:
            next_button = tk.Button(button_frame, text='>>',
                                    state=tk.DISABLED,
                                    pady=40,
                                    padx=40,
                                    bg='green',
                                    )
            next_button.grid(row=0, column=2)

        # keep window \\ configure all widgets corresponding to the article
        def change_article(forward=True):
            nonlocal node
            nonlocal label_title
            nonlocal text
            nonlocal content
            nonlocal prev_button
            nonlocal next_button

            #update node
            if forward:
                node = node.next
            else:
                node = node.prev
            content = soups.article(node.data)
            # change title label
            label_title.config(text='\n'.join(content[0]['titles']))

            #change text.Text string
            text.delete('1.0', 'end')
            for p in content[1]:
                text.insert(tk.END, format_article(p, 40))
            for key, val in content[0].items():
                if key!='titles':
                    text.insert(tk.END, '{} : {}\n'.format(key, val))
            # update state next_button
            if node.next:
                next_button.config(state=tk.NORMAL)
            else:
                next_button.config(state=tk.DISABLED)

            # update state prev_button
            if node.prev:
                prev_button.config(state=tk.NORMAL)
            else:
                prev_button.config(state=tk.DISABLED)



#Section
def newWindow(s):
    global topic
    global doubly_ll
    doubly_ll = dll.DoublyLinkedList()
    doubly_ll.arr_to_list(soups.heads(s).keys())
    topic = tk.Toplevel(root)
    topic.title(s.capitalize())
    topic.geometry('700x500')
    topic.config(bg='blue')

    content = soups.heads(s)
    lst_button = []
    lst_label = []

    for idx, key in enumerate(content):

        lst_label.append(tk.Label(topic,text='\n'.join(content.get(key))))
        lst_button.append(tk.Button(topic, text='mehr Lesen', command=lambda key=key: articleWindow(key)))
        lst_label[idx].grid(row=idx, column=0, padx=5, pady=5)
        lst_button[idx].grid(row=idx, column=1, padx=5, pady=5)

# Main Window
def main():
    global root

    #root config
    root = tk.Tk()
    root.geometry('960x620')
    root.title('ZDF Nachrichten')
    root.config(bg='orange')
    # Sport Section
    button1 = ttk.Button(root, text='Sport', command= lambda: newWindow('sport'))
    button1.pack(side='top', pady=10)

    # Politik Section
    button2 = ttk.Button(root, text='Politik', command= lambda: newWindow('politik'))
    button2.pack(side='top', pady=10)

    #Panorama Section
    button3 = ttk.Button(root, text='Panorama', command= lambda: newWindow('panorama'))
    button3.pack(side='top', pady=10)

    # Wirtschaft Section
    button4 = ttk.Button(root, text='Wirtschaft', command= lambda: newWindow('wirtschaft'))
    button4.pack(side='top', pady=10)

    #quit button
    quit_button = ttk.Button()
    quit_button.pack(side='bottom')

    quit_button.configure(text='Quit', command=root.destroy)

    button_style = ttk.Style()
    button_style.configure('TButton', font=('helvetica', 20, 'bold'), borderwidth='20')

    root.mainloop()


if __name__ == '__main__':
    main()

##test if push works in pycharm