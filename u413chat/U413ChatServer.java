//   **************************************************************************
//   *                                                                        *
//   *  This program is free software: you can redistribute it and/or modify  *
//   *  it under the terms of the GNU General Public License as published by  *
//   *  the Free Software Foundation, either version 3 of the License, or     *
//   * (at your option) any later version.                                    *
//   *                                                                        *
//   *  This program is distributed in the hope that it will be useful,       *  
//   *  but WITHOUT ANY WARRANTY; without even the implied warranty of        *
//   *  MERCHANTABILITY || FITNESS FOR A PARTICULAR PURPOSE.  See the         *
//   *  GNU General Public License for more details.                          *
//   *                                                                        *
//   *  You should have received a copy of the GNU General Public License     *
//   *  along with this program.  If not, see <http://www.gnu.org/licenses/>. *
//   *                                                                        *
//   *                   (C) Arvind Kumar 2011 .                              *
//   **************************************************************************
//This is the first program where im commenting stuff out to make the readers undertsnad more clearly. I'm sorry if thats irritating.

import java.io.*; //streams
import java.net.*; //sockets
import java.util.*; //Other weird Classes
import java.util.concurrent.*; //For LinkedBlockingQueue
import java.sql.*; //For MYSQL stuff

public class U413ChatServer implements Runnable{ //threads run in same class. I tried to make it such that everything fits in just one file.
	
	//each instance will have their respective information
	private static Socket socket; 
    private String username;
    private String nick;
	public static final Object synch = new Object(); //synchronized such that only one thread can use a block at a time
	public static Map<String, U413ChatServer> connectionMap = new HashMap<String, U413ChatServer>(); //lists individual connections
    public static Map<String, Channel> channelMap = new HashMap<String, Channel>(); //lists individual channels
	
	public U413ChatServer(Socket socket){ //default contsructor
        this.socket = socket;
    }
	
	public static void main(String args[]){
		BufferedReader b=new BufferedReader(new InputStreamReader(System.in));
		System.out.print("PORT ( default - 1000 ): "); //choose port. Any error will make it 1000 by default
		int port=1000;
		try{
			port=Integer.parseInt(b.readLine()); //retards might type space or alphanumeric keys
		}
		catch(Exception e){
			System.out.println("Wrong format. Using 1000 instead"); //if they're retard enough to make it into this block , then tell them on their face that you aint giving them another chance
			port=1000;
		}
		System.out.println("Server Started. Waiting for connections");
		try{
			ServerSocket listener=new ServerSocket(port);
			while(true){
				Socket server=listener.accept();
				U413ChatServer connection=new U413ChatServer(server); //heres when each individual connection starts an instance
				Thread t=new Thread(connection); //and then starts a thread for itself simultaneously
				t.start();
			}
		}
		catch(Exception e){ e.printStackTrace();
			System.out.println("Error : Cannot start server on port - "+port+" Quiting."); //other applications running on same port my cause problems
		}
	}
	
	public void run(){
		try{
			startServ(); //main stuff
		}
		catch(Exception e){ //client might close without giving any prior information
			if (nick!=null&&connectionMap.get(nick)==this){ //if everything is what its supposed to be , then remove the connection like how its supposed to be removed
                try{
					sendQuit("Leaving");
				}
				catch(Exception ex){ }
            }
			connectionMap.remove(this);
			System.out.println(nick+" closed the connection");
			e.printStackTrace();
		}
	}
	
	public void startServ()throws Exception{
        checkSendLoop.start(); //make sure any changes to the send queue are sent instantly
        String comm;
		OutputStream out=socket.getOutputStream();
		
		BufferedReader reading=new BufferedReader(new InputStreamReader(socket.getInputStream()));
        while((comm=reading.readLine())!=null){ //all text from client is taken here
            evaluate(comm); //evaluate it
        }
    }
	
	//Better method for sending data to client. Any change to outQueue and all data will be immediately sent.
	LinkedBlockingQueue<String> outQueue=new LinkedBlockingQueue<String>(1000);
	
	public Thread checkSendLoop=new Thread(){ //this is done to cramp everything in one file. Also more neater
        public void run(){
            try{
				OutputStream out=socket.getOutputStream();
                while (true){
                    String mes=outQueue.take();
                    mes=mes.replace("\n", "").replace("\r", ""); //for safety
                    mes=mes+"\r\n"; //append
                    out.write(mes.getBytes());
					out.flush();
                }
            }
            catch (Exception e){
                System.out.println("FATAL : Data to a client will not be sent anymore."); //probably a socket close threw the exception
                outQueue.clear();
                outQueue=null;
            }
        }
    };
	
	public void evaluate(String line)throws Exception{
        System.out.println("Evaluating - "+nick+": "+line);
        String prefix="";
        String[] split=line.split(" ", 2); //split by spaces to 2 strings
        String command=split[0]; //first is command
		if (split.length>1)
			line=split[1]; //rest is args
		else
			line="";
        String[] arguments=line.split(" "); //split args by spaces
        Command commandObject=null; //command object for that respective command
        try{
            commandObject=Command.valueOf(command.toUpperCase()); //set the command object
        }
        catch (Exception e){}
        if (commandObject==null){
            sendSelfNotice("Invalid Command or Not Supported - "+command); //Not supported because it might be supported in the future
            return;
        }
        if (arguments.length<commandObject.getMin()||arguments.length>commandObject.getMax()){
            sendSelfNotice("Invalid Arguments"); //up to user to realize what this means
            return;
        }
		U413ChatServer testcon=connectionMap.get(nick); //dont accept commands if user hasnt set AUTH yet
		if (testcon!=this&&(!command.toUpperCase().equals("AUTH")))
			sendSelfNotice("You are not authenticated");
		else
			commandObject.run(this, prefix, arguments); //Execute command
    }
	
	public void sendQuit(String mess)throws Exception{ //Function to quit properly
        synchronized (synch){
            for (String channelName : new ArrayList<String>(channelMap.keySet())){
                Channel channel=channelMap.get(channelName);
                channel.channelMembers.remove(this); //remove this from the channel members list
                channel.send("LOGOUT "+nick); //tell everyone hes out
                if (channel.channelMembers.size()==0&&(!channel.persist))
                    channelMap.remove(channel.name); //remove channel on leaving
				connectionMap.remove(this);
				socket.close();
            }
        }
    }
	
	public void sendSelfNotice(String string){
        send("NOTICE "+string.replace("%","%25").replace(" ","%20")); //Errors , modes , stuff like that
    }
	
	public void send(String s){
        Queue<String> testQueue = outQueue;
		s=s+" "+getUnixTime();
        if (testQueue!=null){
            System.out.println("SENDING "+nick+" - "+s);
            testQueue.add(s); //just add to the queue , the check loop will make sure that its sent
        }
    }
	
	public String getUnixTime(){
		return ""+(System.currentTimeMillis()/1000L);
	}
	
	public static class Channel{
        ArrayList<U413ChatServer> channelMembers=new ArrayList<U413ChatServer>(); //Connection objects of Channel Members
		ArrayList<U413ChatServer> channelops=new ArrayList<U413ChatServer>(); //Connection objects of Channel Ops
		ArrayList<String> banlist=new ArrayList<String>(); //list of nicks of the banned users
        String topic;
        String name;
		boolean persist=false;
        
        public void sendNot(U413ChatServer not, String toSend){ //send to everyone in channel except to the sender
            synchronized (synch){
                for (U413ChatServer con : channelMembers){
                    if (con != not)
                        con.send(toSend);
                }
            }
        }
        
        public void send(String toSend){ //send to everyone in channel
            sendNot(null, toSend);
        }
    }
	
	public enum Command{
		AUTH(1, 1){
			public void run(U413ChatServer con, String prefix, String[] arguments)throws Exception{
				String url="jdbc:mysql://localhost:3306/u413"; //setting up stuff for MySQL connection
				String user="u413";
				File file=new File("/var/u413.pwd"); //read password
				int ch;
				StringBuffer strContent=new StringBuffer("");
				try{
					FileInputStream fin=new FileInputStream(file);
					while ((ch=fin.read())!=-1)
						strContent.append((char) ch);
					fin.close();
				}
				catch (Exception e) {}
				String password=strContent.toString().replace("\n", "").replace("\r", "").replace(" ", "");
				String name="";
				int userid=0,access=0;
				try{
					Class.forName("com.mysql.jdbc.Driver");
					Connection conn=DriverManager.getConnection(url, user, password);
					Statement st=conn.createStatement();
					ResultSet rs=st.executeQuery("SELECT * FROM sessions WHERE id='"+arguments[0]+"';"); //execute query
					while (rs.next()) { //get rows
						userid=rs.getInt("user");
						name=rs.getString("username");
						access=rs.getInt("access"); 
					}
					st.close();
					conn.close();
				}
				catch(Exception e){ e.printStackTrace();
					userid=0;
					name="";
					access=0;
				}
				if (name.equals("")){ //somethings gone really wrong - client isnt supposed to send invalid session
					userid=0;
					name="Guest";
					access=0;
					con.send("AUTH Guest");
					con.send("LOGOUT Bye");
					con.sendQuit("Invalid");
					connectionMap.remove(this);
				}
				else{
					con.nick=name;
					synchronized (synch){
						U413ChatServer testconn=connectionMap.get(con.nick); //test if theres already a similar connection
						if (testconn!=null){
							con.sendSelfNotice("User already logged in. Make sure you have no other windows/tabs open. Otherwise PM a mod or admin");
						}
						else{
							connectionMap.put(con.nick, con); //add the connection
							con.send("AUTH "+con.nick); //send AUTH back to client
							con.sendSelfNotice("Looked up Session. Received User"); //Send Welcome messages and Stuff
							con.sendSelfNotice("**Connection Authenticated and Established**");
							con.sendSelfNotice("*");
							con.sendSelfNotice("Welcome to U413's Epic Chat Server. "+con.nick);
							con.sendSelfNotice("Written by EnKrypt");
							con.sendSelfNotice("*");
							con.sendSelfNotice("Type '/JOIN <channel>' to join a channel");
						}
					}
				}
			}
		},
		JOIN(1, 1){
			public void run(U413ChatServer con, String prefix, String[] arguments)throws Exception{
				String[] channelNames=arguments[0].split(","); //join mutliples chanells in one line
                for (String channelName : channelNames){
                    if (channelName.contains(" ")){
						con.sendSelfNotice("Channel name cannot have spaces");
					}
					synchronized (synch){
						Channel channel=channelMap.get(channelName);
						boolean added=false;
						if (channel==null){
							added=true;
							channel=new Channel(); //create channel
							channel.name=channelName;
							channelMap.put(channelName, channel);
						}
						if (channel.channelMembers.contains(con)){ //dont rejoin
							con.sendSelfNotice("You're already a member of "+channelName);
							return;
						}
						if (channel.banlist.contains(con.nick)){ //hes banned from that channel
							con.sendSelfNotice("You've been banned from "+channelName);
							return;
						}
						channel.channelMembers.add(con); //add connection object
						channel.send("JOIN "+channelName+" "+con.nick); //tell other you've joined
						String url="jdbc:mysql://localhost:3306/u413"; //setting up stuff for MySQL connection
						String user="u413";
						File file=new File("/var/u413.pwd"); //read password
						int ch;
						StringBuffer strContent=new StringBuffer("");
						try{
							FileInputStream fin=new FileInputStream(file);
							while ((ch=fin.read())!=-1)
								strContent.append((char) ch);
							fin.close();
						}
						catch (Exception e) {}
						String password=strContent.toString().replace("\n", "").replace("\r", "").replace(" ", "");
						int access=0;
						try{
							Class.forName("com.mysql.jdbc.Driver");
							Connection conn=DriverManager.getConnection(url, user, password);
							Statement st=conn.createStatement();
							ResultSet rs=st.executeQuery("SELECT * FROM sessions WHERE id='"+arguments[0]+"';"); //execute query
							while (rs.next()) { //get rows
								access=rs.getInt("access"); 
							}
							st.close();
							conn.close();
						}
						catch(Exception e){ 
							access=10;
						}
						if (added||access>20){ //user might be a mod or admin of u413
							channel.channelops.add(con); //creator becomes op
							channel.send("OP "+channelName+" "+con.nick);
						}
						String listop="OPS "+channelName;
						for (U413ChatServer channelop : channel.channelops){ //give list of ops
							listop+=" "+channelop.nick;
						}
						con.send(listop);
						String listmem="USERS "+channelName;
						for (U413ChatServer channelMember : channel.channelMembers){ //give list of members
							listmem+=" "+channelMember.nick;
						}
						con.send(listmem);
						if (channel.topic!=null) //give topic
							con.send("TOPIC "+arguments[0]+" "+channel.topic.replace("%","%25").replace(" ","%20"));
						else
							con.send("TOPIC "+arguments[0]);
					}
				}
			}
		},
		USERS(1, 1){ //get list of users in that channel
			public void run(U413ChatServer con, String prefix, String[] arguments)throws Exception{
				Channel channel=channelMap.get(arguments[0]);
                if (channel==null){
                    con.sendSelfNotice("Invalid Channel - "+arguments[0]);
                    return;
                }
				String listmem="USERS "+arguments[0];
				for (U413ChatServer channelMember : channel.channelMembers){ //give list of members
					listmem+=" "+channelMember.nick;
				}
				con.send(listmem);
            }
		},
		OPS(1, 1){ //get list of ops in that channel
			public void run(U413ChatServer con, String prefix, String[] arguments)throws Exception{
				Channel channel=channelMap.get(arguments[0]);
                if (channel==null){
                    con.sendSelfNotice("Invalid Channel - "+arguments[0]);
                    return;
                }
				String listop="OPS "+arguments[0];
				for (U413ChatServer channelop : channel.channelops){ //give list of ops
					listop+=" "+channelop.nick;
				}
				con.send(listop);
            }
		},
		LOGOUT(1, 1){
			public void run(U413ChatServer con, String prefix, String[] arguments)throws Exception{
				con.send("LOGOUT Bye"); //client will understand this as end of communication
                con.sendQuit("");
            }
		},
		LEAVE(1, 1){
			public void run(U413ChatServer con, String prefix, String[] arguments)throws Exception{
				String[] channelNames=arguments[0].split(",");
                for (String channelName : channelNames){ //leave more than one channel in one command
                    synchronized (synch){
                        Channel channel=channelMap.get(channelName);
                        if (channel==null)
                            con.sendSelfNotice("Invalid Channel");
                        else{
							if (channel.channelMembers.contains(con)){ //leave only if you're part of the channel
								channel.send("LEAVE "+channelName+" "+con.nick);
								channel.channelMembers.remove(con);
								if (channel.channelMembers.size()==0&&(!channel.persist))
									channelMap.remove(channelName); //remove channel if there ae no more users
							}
                        }
                    }
                }
			}
		},
		TOPIC(1,2){
			public void run(U413ChatServer con, String prefix, String[] arguments)throws Exception{
				Channel channel=channelMap.get(arguments[0]);
                if (channel==null){
                    con.sendSelfNotice("Invalid Channel - "+arguments[0]);
                    return;
                }
				if (arguments.length==1){
                    if (channel.topic!=null)
                        con.send("TOPIC "+arguments[0]+" "+channel.topic.replace("%","%25").replace(" ","%20")); //give topic
                    else
                        con.send("TOPIC "+arguments[0]); //give blank topic
                }
				else{
					channel.topic=arguments[1].replace("%20"," ").replace("%25","%"); //set topic 
                    channel.send("TOPIC "+arguments[0]+" "+arguments[1]+" "+con.nick); //give others the topic
				}
			}
		},
		OP(2, 2){
			public void run(U413ChatServer con, String prefix, String[] arguments)throws Exception{
				synchronized (synch){
					Channel channel=channelMap.get(arguments[0]);
					if (channel==null){
						con.sendSelfNotice("Invalid Channel - "+arguments[0]);
						return;
					}
					U413ChatServer opcon=connectionMap.get(arguments[1]);
					if (channel.channelops.contains(con)){ //only ops can make others op
						if (channel.channelops.contains(opcon)){ //he's already op
							con.send(arguments[1]+" is already OP");
						}
						else{
							if (channel.channelMembers.contains(opcon)){
								channel.channelops.add(opcon); //make op
								channel.send("OP "+arguments[0]+" "+arguments[1]); //tell others
							}
							else{
								con.send("Invalid Nick - "+arguments[1]);
							}
						}
					}
					else{
						con.send("Insufficient Previliges");
					}
				}
			}
		},
		DEOP(2, 2){
			public void run(U413ChatServer con, String prefix, String[] arguments)throws Exception{
				synchronized (synch){
					Channel channel=channelMap.get(arguments[0]);
					if (channel==null){
						con.sendSelfNotice("Invalid Channel - "+arguments[0]);
						return;
					}
					U413ChatServer opcon=connectionMap.get(arguments[1]);
					if (channel.channelops.contains(con)){ //only ops can make others deop
						if (!channel.channelops.contains(opcon)){ //he's not op
							con.send(arguments[1]+" is not OP");
						}
						else{
							if (channel.channelMembers.contains(opcon)){
								channel.channelops.remove(opcon); //make op
								channel.send("DEOP "+arguments[0]+" "+arguments[1]); //tell others
							}
							else{
								con.send("Invalid Nick - "+arguments[1]);
							}
						}
					}
					else{
						con.send("Insufficient Previliges");
					}
				}
			}
		},
		SEND(2,2){
			public void run(U413ChatServer con, String prefix, String[] arguments)throws Exception{
				Channel channel=channelMap.get(arguments[0]);
                if (channel==null){
                    con.sendSelfNotice("Invalid Channel - "+arguments[0]);
                    return;
                }
				else if (!channel.channelMembers.contains(con))  //you need to be part of a channel if you want to chat in it
					con.sendSelfNotice("You are not part of "+arguments[0]);
				else{
					channel.send("SEND "+arguments[0]+" "+arguments[1]+" "+con.nick); //Send message to all members including sender
				}
			}
		},
		ME(2,2){ //same as SEND , will be interpreted differently by Client
			public void run(U413ChatServer con, String prefix, String[] arguments)throws Exception{
				Channel channel=channelMap.get(arguments[0]);
                if (channel==null){
                    con.sendSelfNotice("Invalid Channel - "+arguments[0]);
                    return;
                }
				else if (!channel.channelMembers.contains(con))
					con.sendSelfNotice("You are not part of "+arguments[0]);
				else{
					channel.send("ME "+arguments[0]+" "+arguments[1]+" "+con.nick);
				}
			}
		},
		PM(2,2){ //It functions like SEND , only it sends messages to a User and not a channel
			public void run(U413ChatServer con, String prefix, String[] arguments)throws Exception{
				U413ChatServer sendcon=connectionMap.get(arguments[0]);
                if (sendcon==null)
                    con.sendSelfNotice("No such user online - "+arguments[0]);
                else
                    sendcon.send("PM "+arguments[0]+" "+arguments[1]+" "+con.nick);
			}
		},
		KICK(2, 3){
			public void run(U413ChatServer con, String prefix, String[] arguments)throws Exception{
				synchronized (synch){
					Channel channel=channelMap.get(arguments[0]);
					if (channel==null){
						con.sendSelfNotice("Invalid Channel - "+arguments[0]);
						return;
					}
					U413ChatServer kickcon=connectionMap.get(arguments[1]);
					if (channel.channelops.contains(con)){ //you need to be op to kick
						if (channel.channelMembers.contains(kickcon)){
							channel.channelMembers.remove(kickcon); //kick him out
							if (arguments.length==2){ //no reason
								channel.send("KICK "+arguments[0]+" "+arguments[1]);
								kickcon.send("KICK "+arguments[0]+" "+arguments[1]);
							}
							if (arguments.length==3){ //reason is given
								channel.send("KICK "+arguments[0]+" "+arguments[1]+" "+arguments[2].replace("%","%25").replace(" ","%20"));
								kickcon.send("KICK "+arguments[0]+" "+arguments[1]+" "+arguments[2].replace("%","%25").replace(" ","%20"));
							}
						}
						else{
							con.sendSelfNotice(arguments[1]+" is not a member of "+arguments[0]);
						}
					}
					else{
						con.sendSelfNotice("Insufficient Previleges");
					}
				}
			}
		},
		BAN(2, 3){
			public void run(U413ChatServer con, String prefix, String[] arguments)throws Exception{
				synchronized (synch){
					Channel channel=channelMap.get(arguments[0]);
					if (channel==null){
						con.sendSelfNotice("Invalid Channel - "+arguments[0]);
						return;
					}
					U413ChatServer bancon=connectionMap.get(arguments[1]);
					if (channel.channelops.contains(con)){ //you need to be op to ban
						if (channel.channelMembers.contains(bancon)){
							channel.channelMembers.remove(bancon);
							channel.banlist.add(bancon.nick); //add him to the banlist
							if (arguments.length==2){ //no reason
								channel.send("BAN "+arguments[0]+" "+arguments[1]);
								bancon.send("BAN "+arguments[0]+" "+arguments[1]);
							}
							if (arguments.length==3){ //reason is given
								channel.send("BAN "+arguments[0]+" "+arguments[1]+" "+arguments[2].replace("%","%25").replace(" ","%20"));
								bancon.send("BAN "+arguments[0]+" "+arguments[1]+" "+arguments[2].replace("%","%25").replace(" ","%20"));
							}
						}
						else{
							con.sendSelfNotice(arguments[1]+" is not a member of "+arguments[0]);
						}
					}
					else{
						con.sendSelfNotice("Insufficient Previleges");
					}
				}
			}
		},
		UNBAN(2, 3){
			public void run(U413ChatServer con, String prefix, String[] arguments)throws Exception{
				synchronized (synch){
					Channel channel=channelMap.get(arguments[0]);
					if (channel==null){
						con.sendSelfNotice("Invalid Channel - "+arguments[0]);
						return;
					}
					U413ChatServer bancon=connectionMap.get(arguments[1]);
					if (channel.channelops.contains(con)){ //you need to be op to unban
						channel.banlist.remove(bancon.nick); //remove nick from banlist
						if (arguments.length==2){ //no reason
							channel.send("UNBAN "+arguments[0]+" "+arguments[1]);
							bancon.send("UNBAN "+arguments[0]+" "+arguments[1]);
						}
						if (arguments.length==3){ //reason is given
							channel.send("UNBAN "+arguments[0]+" "+arguments[1]+" "+arguments[2].replace("%","%25").replace(" ","%20"));
							bancon.send("UNBAN "+arguments[0]+" "+arguments[1]+" "+arguments[2].replace("%","%25").replace(" ","%20"));
						}
					}
					else{
						con.sendSelfNotice("Insufficient Previleges");
					}
				}
			}
		},
		PERSIST(1, 1){ //channel will not get removed if there are no more users
			public void run(U413ChatServer con, String prefix, String[] arguments)throws Exception{
				synchronized (synch){
					Channel channel=channelMap.get(arguments[0]);
					if (channel==null){
						con.sendSelfNotice("Invalid Channel - "+arguments[0]);
						return;
					}
					if (channel.channelops.contains(con)){ //you need to be op to do this
						channel.persist=true;
						con.send("PERSIST "+arguments[0]); //tell sender that persist was successful
					}
					else{
						con.sendSelfNotice("Insufficient Previleges");
					}
				}
			}
		},
		PING(1, 1){
            public void run(U413ChatServer con, String prefix, String[] arguments)throws Exception{
                con.send("PONG "+arguments[0]); //return same argument
            }
        };
		int minArgumentCount; //minimum number of arguments for the command
        int maxArgumentCount; //maximum number of arguments for the command
        
        Command(int min, int max){
            minArgumentCount = min;
            maxArgumentCount = max;
        }
        
        public int getMin(){
            return minArgumentCount;
        }
        
        public int getMax(){
            return maxArgumentCount;
        }
		
		public abstract void run(U413ChatServer con, String prefix, String[] arguments) throws Exception; //runs command
	}
}