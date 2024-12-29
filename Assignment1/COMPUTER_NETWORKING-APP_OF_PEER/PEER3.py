
from tkinter import *
import tkinter as tk
# from customtkinter import CTkButton
import customtkinter as ctk
from tkinter import messagebox
import socket
from threading import Thread
import pickle
import threading
import os
import math


WIDTH = 900
HEIGHT = 600
subFileSize= 512*1024 # 512KB

#----------------------------------------Start front end-------------------------------
class SlidePanel(ctk.CTkFrame):
  def __init__(self,parent,start_pos,end_pos):
      super().__init__(master=parent)
      
      self.start_pos=start_pos
      self.end_pos=end_pos
      self.width = abs(start_pos-end_pos)
      
      self.pos = start_pos
      self.in_start_pos = True
      
      self.place(relx=self.start_pos,rely=0,relwidth=self.width,relheight=0.65)
      
  def animate(self):
      if self.in_start_pos:
          self.animate_forward()
      else:
          self.animate_backward()
  def animate_forward(self):
      if self.pos > self.end_pos:
          self.pos -= 0.008
          self.place(relx=self.pos,rely=0,relwidth=self.width,relheight=0.65)
          self.after(10,self.animate_forward)
      else:
          self.in_start_pos = False
  def animate_backward(self):
      if self.pos < self.start_pos:
          self.pos += 0.008
          self.place(relx=self.pos,rely=0,relwidth=self.width,relheight= 0.65)
          self.after(10,self.animate_backward)
      else:
          self.in_start_pos = True

class PEER_FE(ctk.CTk):
  
  def __init__(self, peerHost, peerPort):
    super().__init__()
    self.username = None
    self.password = None
    
    self.numberOfFileUploaded= 0
    self.numberOfFileDownloaded= 0
    
    self.fileUploaded= []
    self.fileDownloaded= []
    self.fileExist= []

    self.peerHost= peerHost
    self.peerPort= peerPort
    
    #---------------------------initial frame for each page-----------------------------
    self.frameInitialPage= ctk.CTkFrame(self,width= 1020, height=700)
    self.frameExecuteLoginButton= ctk.CTkFrame(self,width=WIDTH,height=HEIGHT)
    self.frameConnectToServer= ctk.CTkFrame(self,width=WIDTH,height=HEIGHT)
    self.frameMainPage= ctk.CTkFrame(self,width=WIDTH,height=HEIGHT)
    self.frameExecuteUploadButton= ctk.CTkFrame(self,width=WIDTH,height=HEIGHT)
    self.frameExecuteDownloadButton= ctk.CTkFrame(self,width=WIDTH,height=HEIGHT)
    
    
    self.textFileExist= ctk.CTkTextbox(self.frameExecuteDownloadButton)
    
    self.animatePanelDownload = SlidePanel(self.frameExecuteDownloadButton, 1,0.7)
    self.outputFileDownload = ctk.CTkTextbox(self.animatePanelDownload)
    
    self.animatePaneUpload = SlidePanel(self.frameExecuteUploadButton, 1,0.7)
    self.outputFileUpload = ctk.CTkTextbox(self.animatePaneUpload)

    self.ServerHost = None
    self.ServerPort = None

    self.resizable(False,False)
    self.title("Bittorrent File Sharing")
    self.geometry("900x600")
  
    self.current_frame = self.initialPage()
    self.current_frame.pack()  
    
  def switch_frame(self, frame):
    self.current_frame.pack_forget()
    self.current_frame = frame()
    self.current_frame.pack(padx = 0) 
    
  def changeTheme(self):
    type = ctk.get_appearance_mode()
    if(type=="Light"):
        ctk.set_appearance_mode("dark")
    else:
        ctk.set_appearance_mode("light")
    
  def initialPage(self):
    
    frame_label = ctk.CTkLabel(self.frameInitialPage, text="WELCOME TO\n BITTORENT FILE SHARING", font=("Arial",40,"bold"))
    frame_label.place(relx=0.5,rely=0.4,anchor=tk.CENTER)

    button_sign_in = ctk.CTkButton(self.frameInitialPage, text="LOG IN", font=("Arial", 15, "bold"),
                                    command=lambda:self.switch_frame(self.executeLoginButton))
    button_sign_in.place(relx=0.4,rely=0.7,anchor=tk.CENTER)
    
    button_sign_up = ctk.CTkButton(self.frameInitialPage, text="CHANGE THEME", font=("Arial", 15, "bold"), command= self.changeTheme)
    button_sign_up.place(relx=0.6,rely=0.7,anchor=tk.CENTER)
    
    return self.frameInitialPage

  def executeLoginButton(self):
    
    home_page = ctk.CTkButton(self.frameExecuteLoginButton, text="HOME PAGE", font=("Arial",20,"bold"),
                              command= lambda:self.switch_frame(self.initialPage) )
    home_page.place(relx = 0.5, rely = 0.15, anchor = tk.CENTER)
    
    label_login = ctk.CTkLabel(self.frameExecuteLoginButton, text="LOG IN", font=(("Arial",30,"bold")))
    label_login.place(relx= 0.5,rely= 0.4,anchor = tk.CENTER)

    label_username = ctk.CTkLabel(self.frameExecuteLoginButton, text="Username", font=("Arial",20,"bold"))
    label_username.place(relx = 0.2, rely=0.5, anchor = tk.CENTER)
    
    username_entry = ctk.CTkEntry(self.frameExecuteLoginButton, placeholder_text="Username", width=300, height=4, show= "***********")
    username_entry.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)

    label_password = ctk.CTkLabel(self.frameExecuteLoginButton, text="Password", font=("Arial",20,"bold"))
    label_password.place(relx = 0.2, rely=0.6, anchor = tk.CENTER)
    
    password_entry = ctk.CTkEntry(self.frameExecuteLoginButton, placeholder_text="Password", width=300, height=4, show = "***************")
    password_entry.place(relx = 0.5, rely = 0.6, anchor = tk.CENTER)

    button_sign_in = ctk.CTkButton(self.frameExecuteLoginButton, text="CONFIRM", font=("Arial",15,"bold"), 
                                    command= lambda:self.executeConfirmButton(username_entry, password_entry))
    button_sign_in.place(relx = 0.5, rely = 0.7, anchor = tk.CENTER)
    
    return self.frameExecuteLoginButton

  def executeConfirmButton(self, usernameEntry, passwordEntry):
    self.username= usernameEntry.get()
    self.password= passwordEntry.get()

    self.switch_frame(self.connectToServer)
    
  def connectToServer(self):
      
    home_page = ctk.CTkLabel(self.frameConnectToServer, text="JOIN TO NETWORK", font=("Arial",40,"bold"))
    home_page.place(relx = 0.5, rely = 0.3, anchor = tk.CENTER)
  
    serverHost = ctk.CTkLabel(self.frameConnectToServer, text="Server host", font=("Arial",20,"bold"))
    serverHost.place(relx = 0.2, rely=0.5, anchor = tk.CENTER)
    
    serverHostEntry = ctk.CTkEntry(self.frameConnectToServer, placeholder_text="Host", width=300, height=7)
    serverHostEntry.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)

    serverPort = ctk.CTkLabel(self.frameConnectToServer, text="Server port", font=("Arial",20,"bold"))
    serverPort.place(relx = 0.2, rely=0.6, anchor = tk.CENTER)
    
    serverPortEntry = ctk.CTkEntry(self.frameConnectToServer, placeholder_text="Port", width=300, height=7)
    serverPortEntry.place(relx = 0.5, rely = 0.6, anchor = tk.CENTER)

    button_sign_in = ctk.CTkButton(self.frameConnectToServer, text="CONNECT TO SERVER", font=("Arial",15,"bold"), 
                                    command= lambda:self.executeConnectToServerButton(serverHostEntry, serverPortEntry))
    button_sign_in.place(relx = 0.5, rely = 0.8, anchor = tk.CENTER)
    
    return self.frameConnectToServer
  
  def executeConnectToServerButton(self, serverHost, serverPort):
    self.ServerHost= str(serverHost.get())
    self.ServerPort= int(serverPort.get())
    
    PEER_BEObject.serverHost= self.ServerHost
    PEER_BEObject.serverPort= self.ServerPort
    
    PEER_BEObject.implementJoinToLAN()
    
    messagebox.showinfo("Successful", "Connected to Server!")
    self.switch_frame(self.mainPage)
    
  def mainPage(self):
      
    frame_label = ctk.CTkLabel(self.frameMainPage, text="THE MAIN FUNCTION", font=("Arial",40,"bold"))
    frame_label.place(relx=0.5,rely=0.2,anchor=tk.CENTER)
    
    frame_label = ctk.CTkLabel(self.frameMainPage, text="INFORMATION OF PEER", font=("Arial",20, "bold"))
    frame_label.place(relx=0.5,rely=0.4,anchor=tk.CENTER)
    
    frame_label = ctk.CTkLabel(self.frameMainPage, text="Peer Host: "+ self.peerHost, font=("Arial", 15 ))
    frame_label.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
    
    frame_label = ctk.CTkLabel(self.frameMainPage, text="Peer Port: "+ str(self.peerPort), font=("Arial", 15))
    frame_label.place(relx=0.5,rely=0.55,anchor=tk.CENTER)
    
    #----------------Button UPLOAD---------------------------------------------------------
    self.btn_upload = ctk.CTkButton(self.frameMainPage, text="UPLOAD", font=("Arial", 20, "bold"),
                                    command=lambda:self.switch_frame(self.executeUploadButton))
    self.btn_upload.place(relx=0.3,rely = 0.7,anchor =tk.CENTER)
    #---------------------------------------------------------------------------------------
    
    #---------------------------Button DOWNLOAD----------------------------------------------
    self.btn_download = ctk.CTkButton(self.frameMainPage, text="DOWNLOAD", font=("Arial", 20, "bold"),
                                        command=lambda:self.switch_frame(self.executeDownloadButton))
    self.btn_download.place(relx=0.5,rely = 0.7,anchor =tk.CENTER)
    #----------------------------------------------------------------------------------------
    
    #----------------------------Button CHANGE THEME--------------------------------------------------------
    self.btn_show_listpeer = ctk.CTkButton(self.frameMainPage, text="CHANGE THEME", font=("Arial", 20, "bold"),
                                            command= self.changeTheme)
    self.btn_show_listpeer.place(relx= 0.7,rely=0.7,anchor = tk.CENTER)
    #--------------------------------------------------------------------------------------------------
  
    return self.frameMainPage
  
  def executeUploadButton(self):

    header_upload = ctk.CTkLabel(self.frameExecuteUploadButton, text="UPLOAD FILE", font=("Arial", 40,"bold"))
    header_upload.place(relx = 0.5,rely=0.3,anchor = CENTER)
    
    self.outputFileUpload.place(relx=0.5,rely=0.55,anchor=ctk.CENTER,relwidth=0.8,relheight=0.8)
    self.outputFileUpload.configure(state=DISABLED)

    upload_label = ctk.CTkLabel(self.frameExecuteUploadButton, text="Enter your path of file", font=("Arial", 20,"bold"))
    upload_label.place(relx = 0.5, rely=0.45,anchor = tk.CENTER)

    upload_entry = ctk.CTkEntry(self.frameExecuteUploadButton, width=300, height= 10, placeholder_text="Enter path to file")
    upload_entry.place(relx = 0.5, rely=0.5,anchor = tk.CENTER)
    
    btn_BACK= ctk.CTkButton(self.frameExecuteUploadButton,text="BACK", font=("Arial", 20,"bold"),
                          command =lambda: self.switch_frame(self.mainPage))
    btn_BACK.place(relx= 0.3, rely= 0.7, anchor= tk.CENTER)
    
    btn_upload = ctk.CTkButton(self.frameExecuteUploadButton, text="UPLOAD", font=("Arial", 20,"bold"),
                                command=lambda:(self.getFileUpload(upload_entry)))      
    btn_upload.place(relx = 0.5,rely=0.7,anchor = CENTER)
  
    
    btn_view_repo=ctk.CTkButton(self.frameExecuteUploadButton,text="FILE UPLOADED", font=("Arial", 20,"bold"),
                          command =lambda:self.animatePaneUpload.animate())
    btn_view_repo.place(relx= 0.7, rely= 0.7, anchor= tk.CENTER)
    
    list_header=ctk.CTkLabel(self.animatePaneUpload, text = " LIST FILES ", font=("Comic Sans",30,"bold"))
    list_header.place(relx=0.5,rely=0.1,anchor=ctk.CENTER)
    # list_header.pack()

    return self.frameExecuteUploadButton
  
  def getFileUpload(self, upload_entry):
    filePathUpload= upload_entry.get()   # file path
    if os.path.exists(filePathUpload):
      condition= Thread(target= PEER_BEObject.implementUpload, args= [filePathUpload])
      condition.start()
      self.switch_frame(self.executeUploadButton)
    else:
      messagebox.showerror("Error", "File don't exist!")
      
  def showFileUploaded(self, fileName):
    self.outputFileUpload.configure(state=NORMAL)
    self.numberOfFileUploaded+= 1
    self.outputFileUpload.insert(ctk.END, f"{self.numberOfFileUploaded}.   \"{fileName}\"" +"\n\n" )
    self.outputFileUpload.see(ctk.END)
    self.outputFileUpload.configure(state=DISABLED)
    
  def showMoment(self):
    frame = ctk.CTkFrame(self,width=(WIDTH + 120),height=700)

    header_upload = ctk.CTkLabel(frame, text="WAITING A MOMENT!", font=("Arial", 40,"bold"))
    header_upload.place(relx = 0.5,rely=0.5,anchor = CENTER)
    
    return frame
      
  def executeDownloadButton(self):

    header_upload = ctk.CTkLabel(self.frameExecuteDownloadButton, text="DOWNLOAD FILE", font=("Arial", 40,"bold"))
    header_upload.place(relx = 0.5,rely=0.1,anchor = CENTER)
    
    listOfFile = ctk.CTkLabel(self.frameExecuteDownloadButton, text="LIST OF FILES", font=("Arial", 20,"bold"))
    listOfFile.place(relx = 0.5,rely=0.2,anchor = CENTER)
 
    self.textFileExist.place(relx=0.5,rely=0.44,anchor=ctk.CENTER,relwidth=0.3,relheight=0.4)
    self.textFileExist.configure(state=DISABLED)
    self.showFileExist()
    
    self.outputFileDownload.place(relx=0.5,rely=0.55,anchor=ctk.CENTER,relwidth=0.8,relheight=0.8)
    self.outputFileDownload.configure(state=DISABLED)

    upload_label = ctk.CTkLabel(self.frameExecuteDownloadButton, text="Enter your file name", font=("Arial", 20,"bold"))
    upload_label.place(relx = 0.5, rely=0.7,anchor = tk.CENTER)

    upload_entry = ctk.CTkEntry(self.frameExecuteDownloadButton, width=300, height= 10, placeholder_text="Enter file name")
    upload_entry.place(relx = 0.5, rely=0.75,anchor = tk.CENTER)
    
    btn_BACK= ctk.CTkButton(self.frameExecuteDownloadButton,text="BACK", font=("Arial", 20,"bold"),
                          command =lambda: self.switch_frame(self.mainPage))
    btn_BACK.place(relx= 0.3, rely= 0.85, anchor= tk.CENTER)
    
    btn_upload = ctk.CTkButton(self.frameExecuteDownloadButton, text="DOWNLOAD", font=("Arial", 20,"bold"),
                                command=lambda:(self.getFileDownload(upload_entry)))      
    btn_upload.place(relx = 0.5,rely=0.85,anchor = CENTER)
  
    
    btn_view_repo=ctk.CTkButton(self.frameExecuteDownloadButton,text="FILE DOWNLOADED", font=("Arial", 20,"bold"),
                          command =lambda: self.animatePanelDownload.animate())
    btn_view_repo.place(relx= 0.75, rely= 0.85, anchor= tk.CENTER)
    
    list_header=ctk.CTkLabel(self.animatePanelDownload, text = " LIST FILES ", font=("Comic Sans",30,"bold")
                              )
    list_header.place(relx=0.5,rely=0.1,anchor=ctk.CENTER)
    # list_header.pack()

    return self.frameExecuteDownloadButton
  
  def getFileDownload(self, download_entry):
    stringFileNameDownload= str(download_entry.get())
    if stringFileNameDownload== "":
      messagebox.showerror("Error", "File don't exist!")
    else:
      listFileNameDownload= []
      iteratorLeft= 0
      iteratorRight= 0
      while True:
        if iteratorRight == len(stringFileNameDownload) -1:
          listFileNameDownload.append(stringFileNameDownload[iteratorLeft: (iteratorRight+ 1)])
          break
        else:
          if stringFileNameDownload[iteratorRight]== ",":  # file1.txt, file2.txt
            listFileNameDownload.append(stringFileNameDownload[iteratorLeft: iteratorRight])
            iteratorLeft= iteratorRight+ 2
            iteratorRight= iteratorLeft
          else:
            iteratorRight+= 1
      
      for fileNameDownload in listFileNameDownload:  
        condition= Thread(target= PEER_BEObject.implementDownload, args=[fileNameDownload])
        condition.start()
      
      self.switch_frame(self.executeDownloadButton)
  
  def showFileDownloaded(self, fileName):
    self.outputFileDownload.configure(state=NORMAL)
    self.numberOfFileDownloaded+= 1
    self.outputFileDownload.insert(ctk.END, f"{self.numberOfFileDownloaded}:   \"{fileName}\"" +"\n\n" )
    self.outputFileDownload.see(ctk.END)
    self.outputFileDownload.configure(state=DISABLED)

  def showFileExist(self):
    self.fileExist= PEER_BEObject.implementReceiveListFileExist()
    self.textFileExist.configure(state=NORMAL)
    count=1
    self.textFileExist.delete(1.0, ctk.END)
    for file in self.fileExist:
        self.textFileExist.insert(ctk.END, f"{count}:   {file}" +"\n\n" )
        count +=1
    self.textFileExist.see(ctk.END)
    self.textFileExist.configure(state=DISABLED)

#-------------------------------------End Front end-------------------------------------
        
#-------------------------------Backend-----------------------------------------------

class PEER_BE():
  
  def __init__(self, peerHost, peerPort):
    self.serverHost= None
    self.serverPort= None
    
    self.peerHost= peerHost
    self.peerPort= peerPort
    
    self.subFileSize= 512*1024
    
  def seedingFileCompleted(self, filePath):
     #-------------------- socket initial-------------------
    peerConnectServerSocket= socket.socket()
    peerConnectServerSocket.connect((self.serverHost, self.serverPort))
    #-------------------------------------------------------
    
    #------------------ send and receive--------------------
    peerConnectServerSocket.send(bytes("Upload", "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    # --------------------------------------------------------
      
    #--------------Send file Name to server----------------------   
    peerConnectServerSocket.send(bytes(filePath, "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    #---------------------------------------------------------
      
    #----------------Send peerHost and port--------------------
    peerConnectServerSocket.send(bytes(self.peerHost, "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    peerConnectServerSocket.send(bytes(str(self.peerPort), "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    #------------------------------------------------------------
    
    #-------------Send size of file--------------------------------
    sizeOfFile= os.path.getsize(filePath)
    peerConnectServerSocket.send(bytes(str(sizeOfFile), "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    #---------------------------------------------------
    
    #---------------send cancel command to close the connection---------------------
    peerConnectServerSocket.send(bytes("Cancel", "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    #-----------------------------------------------------------------------------
    
    #close the socket
    peerConnectServerSocket.close()
    #-------------------
    
  def implementUpload(self, filePath):
    #-------------------- socket initial-------------------
    peerConnectServerSocket= socket.socket()
    peerConnectServerSocket.connect((self.serverHost, self.serverPort))
    #-------------------------------------------------------
    
    #------------------ send and receive--------------------
    peerConnectServerSocket.send(bytes("Upload", "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    # --------------------------------------------------------
      
    #--------------Send file Name to server----------------------   
    peerConnectServerSocket.send(bytes(filePath, "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    #---------------------------------------------------------
      
    #----------------Send peerHost and port--------------------
    peerConnectServerSocket.send(bytes(self.peerHost, "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    peerConnectServerSocket.send(bytes(str(self.peerPort), "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    #------------------------------------------------------------
    
    #-------------Send size of file--------------------------------
    sizeOfFile= os.path.getsize(filePath)
    peerConnectServerSocket.send(bytes(str(sizeOfFile), "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    #---------------------------------------------------
    
    #---------------send cancel command to close the connection---------------------
    peerConnectServerSocket.send(bytes("Cancel", "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    #-----------------------------------------------------------------------------
    
    #close the socket
    peerConnectServerSocket.close()
    #-------------------
    
    #-----------------get fileName--------------------
    iterator= -1
    while True:
      if filePath[iterator]== "\\":
        break
      else:
        iterator-= 1
    fileName= filePath[(iterator+ 1): ]
    #------------------------------------------------
    messagebox.showinfo("Successful", "Upload file "+ str(fileName)+ " completed!")
    PEER_FEObject.fileUploaded.append(fileName)
    PEER_FEObject.showFileUploaded(fileName)
  
  def implementReceiveListFileExist(self):
    #-------------------- socket initial-------------------
    peerConnectServerSocket= socket.socket()
    peerConnectServerSocket.connect((self.serverHost, self.serverPort))
    #-------------------------------------------------------
    
    #------------------ send and receive--------------------
    peerConnectServerSocket.send(bytes("fileExist", "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    # ----------------------------------------------------
    
    peerConnectServerSocket.send(bytes("SUCCESS", "utf-8"))
    
    #----------------Receive list file exist-----------------------
    listFileExist= pickle.loads(peerConnectServerSocket.recv(10240))
    peerConnectServerSocket.send(bytes("SUCCESS", "utf-8"))
    #---------------------------------------------------------------
    
    peerConnectServerSocket.recv(4096)
    
    #---------------send cancel command to close the connection---------------------
    peerConnectServerSocket.send(bytes("Cancel", "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    #-----------------------------------------------------------------------------
    
    #close the socket
    peerConnectServerSocket.close()
    #-------------------
    
    return listFileExist
  
  def implementJoinToLAN(self):
    #-------------------- socket initial-------------------
    peerConnectServerSocket= socket.socket()
    peerConnectServerSocket.connect((self.serverHost, self.serverPort))
    #-------------------------------------------------------
    
    #------------------ send and receive--------------------
    peerConnectServerSocket.send(bytes("Join to LAN", "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    # ----------------------------------------------------
    
    #-------------------Send inform of peer------------------------
    peerInform= pickle.dumps([self.peerHost, self.peerPort])
    peerConnectServerSocket.sendall(peerInform)
    peerConnectServerSocket.recv(4096) # success
    #--------------------------------------------------------------
    
    peerConnectServerSocket.send(bytes("CONFIRM", "utf-8")) # new insert
    
    #---------------Receive the list of peers-------------------------
    listPeer= pickle.loads(peerConnectServerSocket.recv(4096))
    peerConnectServerSocket.send(bytes("SUCCESS", "utf-8"))  # confirm
    #------------------------------------------------------------------
    
    peerConnectServerSocket.recv(4096)
    
    #---------------send cancel command to close the connection---------------------
    peerConnectServerSocket.send(bytes("Cancel", "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    #-----------------------------------------------------------------------------
    
    #close the socket
    peerConnectServerSocket.close()
    #-------------------
       
  def threadListenServerOrPeers(self, conn, addr, stopFlag):
    while not stopFlag.is_set():
      #----------------Receive Type of connect server or peer-----------------------------
      serverOrPeer = str(conn.recv(4096), "utf-8")
      conn.send(bytes("SUCCESS", "utf-8"))  # confirm
      #-----------------------------------------------------------------------------------

      #---------------Classify the serverOrPeer-----------------------------------------
      if serverOrPeer== "SERVER":
        #-----------------Receive FileName-------------------------------------
        filePartPath= str(conn.recv(4096), "utf-8")
        conn.send(bytes("SUCCESS", "utf-8"))  # confirm
        #---------------------------------------------------------------------
        
        #-------------------------Receive size of file-----------------------------
        sizeOfFile= int(str(conn.recv(4096), "utf-8"))
        conn.send(bytes("SUCCESS", "utf-8"))  # confirm
        #-------------------------------------------------------------------------
  
        #--------------Receive the content of file-------------------------------
        with open(filePartPath, "wb") as file:
          content= b''
          while sizeOfFile > 0:
            data= conn.recv(min(10240, sizeOfFile))
            if not data:
              break
            content+= data
            sizeOfFile-= len(data)
          file.write(content)
          file.close()
        conn.send(bytes("SUCCESS", "utf-8"))  # confirm
        #-------------------------------------------------------------------------
        
        #-----------------------Cancel command------------------------------------
        cancelCommand= str(conn.recv(4096), "utf-8")
        conn.send(bytes("SUCCESS", "utf-8"))  # confirm
        stopFlag.set()
        #-----------------------------------------------------------------------
      else:
        if serverOrPeer== "PEER":
          #-----------Receive file name is requested down from other peer-----------------
          filePath= str(conn.recv(4096), "utf-8")
          conn.send(bytes("SUCCESS", "utf-8"))  # confirm
          #------------------------------------------------------------------------------
          
          #-----------Receive the position of pointer--------------------------
          pointer= int(str(conn.recv(4096), "utf-8"))
          conn.send(bytes("SUCCESS", "utf-8"))
          #--------------------------------------------------------------------------
          
          conn.recv(4096)
          
          #-----------Send file content to the peer's request-------------------------
          with open(filePath, "rb") as file:
            file.seek(pointer)
            subContent= file.read(subFileSize)
            conn.sendall(subContent)
            conn.recv(4096)
            file.close()
          #-----------------------------------------------------------------------------
          
          conn.send(bytes("SUCCESS", "utf-8"))
          
          #-----------------------Cancel command------------------------------------
          cancelCommand= str(conn.recv(4096), "utf-8")
          conn.send(bytes("SUCCESS", "utf-8"))  # confirm
          stopFlag.set()
          #-----------------------------------------------------------------------
    return 
  
  def listenServerOrPeers(self):
    peerSocket= socket.socket()
    peerSocket.bind((self.peerHost, self.peerPort))
    peerSocket.listen(10)
    
    while True:
      conn, addr= peerSocket.accept()
      stopFlag= threading.Event()
      condition= Thread(target= self.threadListenServerOrPeers, args= [conn, addr, stopFlag])
      condition.start()
      
  def implementDownload(self, fileNameDownload):
    
    #-------------------- socket initial-------------------
    peerConnectServerSocket= socket.socket()
    peerConnectServerSocket.connect((self.serverHost, self.serverPort))
    #-------------------------------------------------------
    
    #------------------ send and receive--------------------------------
    peerConnectServerSocket.send(bytes("Download", "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    # --------------------------------------------------------------
    
    #------------------Send List of files want to down------------------------------
    peerConnectServerSocket.sendall(pickle.dumps(fileNameDownload))
    peerConnectServerSocket.recv(4096)
    #-------------------------------------------------------------------
    
    #--------------------Send peerHost and peerPort----------------------
    peerConnectServerSocket.send(bytes(self.peerHost, "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    peerConnectServerSocket.send(bytes(str(self.peerPort), "utf-8"))
    peerConnectServerSocket.recv(4096)  # success
    #--------------------------------------------------------------------
    
    peerConnectServerSocket.send(bytes("SUCCESS", "utf-8"))  # insert

    #-----------------Check file is exist or not------------------------
    condition= str(peerConnectServerSocket.recv(4096), "utf-8")  # complete  # stop
    peerConnectServerSocket.send(bytes("SUCCESS", "utf-8"))  # confirm
    if condition== "File exist!":
      allContent= b''
      #------------Receive list filePath and peer-------------------------------
      listFilePathPeer= pickle.loads(peerConnectServerSocket.recv(10240))
      peerConnectServerSocket.send(bytes("SUCCESS", "utf-8"))
      #-------------------------------------------------------------------------
            
      #---------------Receive number of pieces----------------------------------
      pieces= int(str(peerConnectServerSocket.recv(4096), "utf-8"))
      print(pieces)
      peerConnectServerSocket.send(bytes("SUCCESS", "utf-8"))
      #-------------------------------------------------------------------------
      
      #----------------------close connection with server-------------------------
      peerConnectServerSocket.recv(4096)
      peerConnectServerSocket.send(bytes("Cancel", "utf-8"))
      peerConnectServerSocket.recv(4096)  # success
      
      peerConnectServerSocket.close()
      #---------------------------------------------------------------------------
    
      numberOfPeers= len(listFilePathPeer)
      
      pointer= 0
      piecesRemain= pieces
      iteratorPeer= 0
      while piecesRemain > 0:
        filePath= listFilePathPeer[iteratorPeer%numberOfPeers][0]
        targetPeerHost= listFilePathPeer[iteratorPeer%numberOfPeers][1]
        targetPeerPort= listFilePathPeer[iteratorPeer%numberOfPeers][2]
        print(piecesRemain)
        if targetPeerHost== self.peerHost and targetPeerPort== self.peerPort:
          with open(filePath, 'rb') as file:
            file.seek(pointer)
            data= file.read(subFileSize)
            allContent+= data
            file.close()
        else:   
          #----------------Initial connect to another peer--------------------------
          peerConnectPeerSocket= socket.socket()
          peerConnectPeerSocket.connect((targetPeerHost, targetPeerPort))
          #--------------------------------------------------------------------------
          
          #-----------------Inform the PEER the other peer want to connect------------------
          peerConnectPeerSocket.send(bytes("PEER", "utf-8"))  # 
          peerConnectPeerSocket.recv(4096)  # Success
          #----------------------------------------------------------------------------
          
          #-----------------Send SubFile name to the peer for downloading-----------------
          peerConnectPeerSocket.send(bytes(filePath, "utf-8"))  # 
          peerConnectPeerSocket.recv(4096)  # Success
          #-------------------------------------------------------------------------------
          
          #--------------------Send Pointer position------------------------
          peerConnectPeerSocket.send(bytes(str(pointer), "utf-8"))
          peerConnectPeerSocket.recv(4096)
          #--------------------------------------------------------------------
          
          peerConnectPeerSocket.send(bytes("CONFIRM", "utf-8"))  # new insert
          
          #-----------------------Receive subContent---------------------------
          data= peerConnectPeerSocket.recv(subFileSize)
          peerConnectPeerSocket.send(bytes("SUCCESS", "utf-8"))
          allContent+= data
          #--------------------------------------------------------------------
          
          peerConnectPeerSocket.recv(4096)   # new insert
          
          #-----------------------Send the cancel command------------------------------------------
          peerConnectPeerSocket.send(bytes("Cancel", "utf-8"))  # 
          peerConnectPeerSocket.recv(4096)  # Success
          #-----------------------------------------------------------------------------
          
          #----------------Close the connection--------------------------
          peerConnectPeerSocket.close()
          #-------------------------------
        
        if iteratorPeer%100== 0:
          with open(fileNameDownload, 'ab') as file:
            file.write(allContent)
            allContent= b""
            file.close()
        pointer+= subFileSize
        piecesRemain-= 1
        iteratorPeer+= 1
       
      #-------------Write and save-------------------------------
      with open(fileNameDownload, 'ab') as file:
        file.write(allContent)
        file.close()
      #---------------------------------------------------------
        
      messagebox.showinfo("Successful", "Download file "+ str(fileNameDownload)+" completed!")
      PEER_FEObject.fileDownloaded.append(fileNameDownload)
      PEER_FEObject.showFileDownloaded(fileNameDownload)
      
      filePath= os.path.abspath(fileNameDownload)
      self.seedingFileCompleted(filePath)
    else:
      messagebox.showerror("Error", "File "+ str(fileNameDownload)+ " not exist!")

    #---------------------------------------------------------------------------------------
  
    return
#------------------------------End back end-----------------------------------------------

    
        
if __name__ == "__main__":
  #--------Using when transferring file with Wireless --------------
  peerHost= socket.gethostbyname_ex(socket.gethostname())[2][1]  
  #-----------------------------------------------------------------
  
  #------Using when transferring file with Ethernet----------------
  peerHost= socket.gethostbyname(socket.gethostname())
  #----------------------------------------------------------------
  
  
  peerPort= 1003
  PEER_BEObject= PEER_BE(peerHost, peerPort)
  condition1= Thread(target= PEER_BEObject.listenServerOrPeers)
  condition1.start()
  
  PEER_FEObject = PEER_FE(peerHost, peerPort)
  PEER_FEObject.mainloop()
    