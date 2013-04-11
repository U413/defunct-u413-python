gloflag=0;
usession="";
uname="";

$(function() {
	$(".chat").draggable({ snap: ".bodyframe" }).resizable({
		resize:function(e,ui){
			var height = parseInt(($(".chat").css("height")).replace("px", ""));
			var width = parseInt(($(".chat").css("width")).replace("px", ""));
			if (height<256){
				$(".chat").css("height","256px");
				height=256;
			}
			if (width<434){
				$(".chat").css("width","434px");
				width=434;
			}
			height-=115;
			$(".out").css("height",height+"px");
		}
	});
});

function firsttimeload(){
	$("#socket").html("<applet id='JavaSocketBridge' archive='JavaSocketBridge.jar' code='JavaSocketBridge.class' width='0' height='0'></applet>");
	$(".chat").css("display","block");
	$(".chat").animate({ opacity: 1 }, 2000);
	$(".in").focus();
	$(".Status").html("Type 'START' to connect");
}

function chatshow(show){
	var tempactive=$(".active").html();
	$("."+tempactive).html($("."+tempactive).html()+"<br>"+show)
}

function sendchat(value){
	params=value.split(" ");
	$(".in").val("");
	if (value.toUpperCase()=="START"&&gloflag==0){
		if (socket_connect(document.domain,1000)){
			gloflag=1;
			$(".Status").html("");
			socket_send("AUTH "+usession);
		}
		else{	
			if (usession==null||usession==undefined){
				chatshow("There was a problem while authenticating. Please refresh and try again");
			}
			else{
				chatshow("Connection failed. Make sure you have java enabled in your browser and reload the page. If you are sure there's nothing wong with your side , you may PM any admin/mod to check on the server.");
			}
		}
	}
	else if (value.toUpperCase()=="START"&&gloflag==1){
		chatshow("Chat already loaded");
	}
	else{
		if (gloflag==0){
			chatshow("You must first type 'START' to establish a connection");
		}
		else{
			if ((value.toUpperCase().startsWith("/JOIN")&&value.indexOf(",")!=-1)||(value.toUpperCase().startsWith("/LEAVE")&&value.indexOf(",")!=-1)){
				chatshow("multiple channel operations are not available right now. You can join/leave only one channel at a time");
			}
			if (value.toUpperCase().startsWith("/JOIN")&&value.indexOf("-")!=-1){
				chatshow("Special character not allowed'-'");
			}
			else if (value.toUpperCase()=="/JOIN #STATUS"){
				chatshow("Sorry , that channel is reserved");
			}
			else if ((!value.startsWith("/"))&&$(".active").html()=="Status"){
				chatshow("You must join a channel to chat");
			}
			else if ((!value.startsWith("/"))&&$(".active").html()!="Status"&&(!$(".active").html().startsWith("PM-"))){
				socket_send("SEND #"+$(".active").html()+" "+value.replace(/%/gi,"%25").replace(/ /gi,"%20"));
			}
			else if ((value.toUpperCase().startsWith("/ME"))&&$(".active").html()=="Status"){
				chatshow("You must join a channel to chat");
			}
			else if ((value.toUpperCase().startsWith("/ME"))&&$(".active").html()!="Status"&&(!$(".active").html().startsWith("PM-"))){
				socket_send("ME #"+$(".active").html()+" "+params[1].replace(/%/gi,"%25").replace(/ /gi,"%20"));
			}
			else if (value.toUpperCase().startsWith("/TOPIC")&&params.length>2){
				var comb="";
				for (i=2;i<params.length;i++){
					comb+=" "+params[i];
				}
				comb=comb.substring(1).replace(/%/gi,"%25").replace(/ /gi,"%20");
				socket_send(params[0].substring(1)+" "+params[1]+" "+comb);
			}
			else if (value.toUpperCase().startsWith("/BAN")&&params.length>3){
				var comb="";
				for (i=3;i<params.length;i++){
					comb=" "+params[i];
				}
				comb=comb.substring(1).replace(/%/gi,"%25").replace(/ /gi,"%20");
				socket_send(params[0].substring(1)+" "+params[1]+" "+comb);
			}
			else if (value.toUpperCase().startsWith("/KICK")&&params.length>3){
				var comb="";
				for (i=3;i<params.length;i++){
					comb=" "+params[i];
				}
				comb=comb.substring(1).replace(/%/gi,"%25").replace(/ /gi,"%20");
				socket_send(params[0].substring(1)+" "+params[1]+" "+comb);
			}
			else if (value.toUpperCase().startsWith("/PM")){
				chatshow(notif("Type '/OPEN &lt;nick&gt;' to open a PM chat window"));
			}
			else if (params[0].toUpperCase()=="/OPEN"){
				createfocus("PM-"+params[1]);
				$(".PM-"+params[1]).html($(".PM-"+params[1]).html()+notif("Type '/CLOSE' to close the PM window"));	
			}
			else if (value.toUpperCase()=="/CLOSE"&&(!$(".active").html().startsWith("PM-"))){
				chatshow(notif("You can only close a PM window. To close a channel window , type '/LEAVE &lt;channel name&gt;'"));
			}
			else if (value.toUpperCase()=="/CLOSE"&&($(".active").html().startsWith("PM-"))){
				removechan($(".active").html());
			}
			else if ((!value.startsWith("/"))&&$(".active").html().startsWith("PM-")){
				socket_send("PM "+$(".active").html().substring(3)+" "+value.replace(/%/gi,"%25").replace(/ /gi,"%20"));
				chatshow("&lt;"+uname+"&gt;"+" "+value);
			}
			else if (value.toUpperCase().startsWith("/ME")&&$(".active").html().startsWith("PM-")){
				chatshow(notif("Feature dissabled due to security issues"));
			}
			else{
				socket_send(value.substring(1));
			}
		}
	}
}

function on_socket_get(message){
	parse(message);
}

function notif(text){
	return "<span style=\"color:#d0d0d0;\" class=\"notif\">"+text+"</span>";
}

String.prototype.startsWith = function(needle){
    return(this.indexOf(needle) == 0);
};

function parse(text){
	text=text.replace(/</gi,"&lt;").replace(/>/gi,"&gt;");
	params=text.split(" ");
	if (params[0].toUpperCase()=="AUTH"){
		if (params[1].toUpperCase()=="GUEST"){
			text="Corrupt login. Please login again and then retry";
		}
		else{
			text="Receiving response";
		}
		chatshow(notif(text));
	}
	if (params[0].toUpperCase()=="LOGOUT"&&(params[1].toUpperCase()=="BYE"||params[1].toUpperCase()==uname.toUpperCase())){
		text="Server has closed the connection. Refresh and try 'CHAT' again.";
		$(".in").remove();
		chatshow(notif(text));
	}
	if (params[0].toUpperCase()=="LOGOUT"&&params[1].toUpperCase()!="BYE"&&params[1].toUpperCase()!=uname.toUpperCase()){
		var chan="";
		$(".out > div").each( function(index){
			chan=$(this).attr('class');
			if ($("#"+params[1]+chan).length){
				$("#"+params[1]+chan).remove();
				$("."+chan).html($("."+chan).html()+"<br>"+notif(params[1]+" has Quit chat"));
			}
		});
		
		//finish and flash + java test fully with network bugs
	}
	if (params[0].toUpperCase()=="NOTICE"){
		text=params[1].replace(/%25/gi,"%").replace(/%20/gi," ");
		chatshow(notif(text));
	}
	if (params[0].toUpperCase()=="JOIN"&&params[2]==uname){
		params[1]=params[1].replace("#","");
		createfocus(params[1]);
		$("."+params[1]).html("<div class=\""+params[1]+"users\" style=\"text-align:center; border-left:solid 1px #00FF00; float:right; width:20%; height:90%; padding:5px;\">Users :<br></div>");
		$("."+params[1]+"users").css("height",$(".out").css("height"));
		$("."+params[1]).html($("."+params[1]).html()+notif("Now talking on #"+params[1]));
	}
	if (params[0].toUpperCase()=="JOIN"&&params[2]!=uname){
		params[1]=params[1].replace("#","");
		$("."+params[1]+"users").html($("."+params[1]+"users").html()+"<span id=\""+params[2]+params[1]+"\">"+params[2]+"</span><br>");
		$("."+params[1]).html($("."+params[1]).html()+"<br>"+notif(params[2]+" has joined "+params[1]));
	}
	if (params[0].toUpperCase()=="USERS"){
		params[1]=params[1].replace("#","");
		$("."+params[1]+"users").html("Users :<br>");
		for (i=2;i<params.length-1;i++){
			$("."+params[1]+"users").html($("."+params[1]+"users").html()+"<span id=\""+params[i]+params[1]+"\">"+params[i]+"</span><br>");
		}
	}
	if (params[0].toUpperCase()=="OPS"){
		params[1]=params[1].replace("#","");
		for (i=2;i<params.length-1;i++){
			$("#"+params[i]+params[1]).html("@"+params[i]);
		}
	}
	if (params[0].toUpperCase()=="OP"){
		params[1]=params[1].replace("#","");
		$("#"+params[2]+params[1]).html("@"+params[2]);
		$("."+params[1]).html($("."+params[1]).html()+"<br>"+notif(params[2]+" is now channel OP"));
	}
	if (params[0].toUpperCase()=="DEOP"){
		params[1]=params[1].replace("#","");
		$("#"+params[2]+params[1]).html(params[2]);
		$("."+params[1]).html($("."+params[1]).html()+"<br>"+notif(params[2]+" is not channel OP anymore"));
	}
	if (params[0].toUpperCase()=="TOPIC"&&params.length==3){
		params[1]=params[1].replace("#","");
		$("#"+params[1]+"topic").html(" ");
	}
	if (params[0].toUpperCase()=="TOPIC"&&params.length==4){
		params[1]=params[1].replace("#","");
		params[2]=params[2].replace(/%25/gi,"%").replace(/%20/gi," ");
		$("#"+params[1]+"topic").html(params[2]);
	}
	if (params[0].toUpperCase()=="TOPIC"&&params.length==5){
		params[1]=params[1].replace("#","");
		params[2]=params[2].replace(/%25/gi,"%").replace(/%20/gi," ");
		$("#"+params[1]+"topic").html(params[2]);
		$("."+params[1]).html($("."+params[1]).html()+"<br>"+notif(params[3]+" has changed the topic to "+params[2]));
	}
	if (params[0].toUpperCase()=="LEAVE"&&params[2]==uname){
		params[1]=params[1].replace("#","");
		removechan(params[1]);
	}
	if (params[0].toUpperCase()=="LEAVE"&&params[2]!=uname){
		params[1]=params[1].replace("#","");
		$("#"+params[2]+params[1]).remove();
		$("."+params[1]).html($("."+params[1]).html()+"<br>"+notif(params[2]+" has left the channel"));
	}
	if (params[0].toUpperCase()=="SEND"){
		params[1]=params[1].replace("#","");
		params[2]=params[2].replace(/%25/gi,"%").replace(/%20/gi," ");
		$("."+params[1]).html($("."+params[1]).html()+"<br><span class=\"msg\">&lt;"+params[3]+"&gt; "+params[2]+"</span>");
		$("."+params[1]+"users").css("height","90%");
	}
	if (params[0].toUpperCase()=="ME"){
		params[1]=params[1].replace("#","");
		params[2]=params[2].replace(/%25/gi,"%").replace(/%20/gi," ");
		$("."+params[1]).html($("."+params[1]).html()+"<br><span class=\"msg\">"+params[3]+" "+params[2]+"</span>");
	}
	if (params[0].toUpperCase()=="PM"){
		params[2]=params[2].replace(/%25/gi,"%").replace(/%20/gi," ");
		if (!$("#PM-"+params[1]).length){
			createfocus("PM-"+params[1]);
			$(".PM-"+params[1]).html($(".PM-"+params[1]).html()+"<br>"+notif("Type '/CLOSE' to close the PM window"));
		}
		$(".PM-"+params[1]).html($(".PM-"+params[1]).html()+"<br><span class=\"msg\">&lt;"+params[1]+"&gt; "+params[2]+"</span>");
	}
	if (params[0].toUpperCase()=="KICK"&&params[2]==uname&&params.length==5){
		params[1]=params[1].replace("#","");
		removechan(params[1]);
		chatshow(notif("You have been kicked from "+params[1]+" by "+params[3]+" (no reason)"));
	}
	if (params[0].toUpperCase()=="KICK"&&params[2]!=uname&&params.length==5){
		params[1]=params[1].replace("#","");
		$("#"+params[2]+params[1]).remove();
		$("."+params[1]).html($("."+params[1]).html()+"<br>"+notif(params[2]+" has been kicked from "+params[1]+" by "+params[3]+" (no reason)"));
	}
	if (params[0].toUpperCase()=="KICK"&&params[2]==uname&&params.length==6){
		params[1]=params[1].replace("#","");
		params[4]=params[4].replace(/%25/gi,"%").replace(/%20/gi," ");
		removechan(params[1]);
		chatshow(notif("You have been kicked from "+params[1]+" by "+params[3]+" ("+params[4].replace(/%25/gi,"%").replace(/%20/gi," ")+")"));
	}
	if (params[0].toUpperCase()=="KICK"&&params[2]!=uname&&params.length==6){
		params[1]=params[1].replace("#","");
		params[4]=params[4].replace(/%25/gi,"%").replace(/%20/gi," ");
		$("#"+params[2]+params[1]).remove();
		$("."+params[1]).html($("."+params[1]).html()+"<br>"+notif(params[2]+" has been kicked from "+params[1]+" by "+params[3]+" ("+params[4].replace(/%25/gi,"%").replace(/%20/gi," ")+")"));
	}
	if (params[0].toUpperCase()=="BAN"&&params[2]==uname&&params.length==5){
		params[1]=params[1].replace("#","");
		removechan(params[1]);
		chatshow(notif("You have been banned from "+params[1]+" by "+params[3]+" (no reason)"));
	}
	if (params[0].toUpperCase()=="BAN"&&params[2]!=uname&&params.length==5){
		params[1]=params[1].replace("#","");
		$("#"+params[2]+params[1]).remove();
		$("."+params[1]).html($("."+params[1]).html()+"<br>"+notif(params[2]+" has been banned from "+params[1]+" by "+params[3]+" (no reason)"));
	}
	if (params[0].toUpperCase()=="BAN"&&params[2]==uname&&params.length==6){
		params[1]=params[1].replace("#","");
		params[4]=params[4].replace(/%25/gi,"%").replace(/%20/gi," ");
		removechan(params[1]);
		chatshow(notif("You have been banned from "+params[1]+" by "+params[3]+" ("+params[4].replace(/%25/gi,"%").replace(/%20/gi," ")+")"));
	}
	if (params[0].toUpperCase()=="BAN"&&params[2]!=uname&&params.length==6){
		params[1]=params[1].replace("#","");
		params[4]=params[4].replace(/%25/gi,"%").replace(/%20/gi," ");
		$("#"+params[2]+params[1]).remove();
		$("."+params[1]).html($("."+params[1]).html()+"<br>"+notif(params[2]+" has been banned from "+params[1]+" by "+params[3]+" ("+params[4].replace(/%25/gi,"%").replace(/%20/gi," ")+")"));
	}
	if (params[0].toUpperCase()=="UNBAN"&&params[2]==uname){
		chatshow(notif("You have been unbanned from "+params[1]+" by "+params[3]));
	}
	if (params[0].toUpperCase()=="UNBAN"&&params[2]!=uname){
		chatshow(notif(params[2]+" has been unbanned from "+params[1]+" by "+params[3]));
	}
	if (params[0].toUpperCase()=="PERSIST"){
		chatshow(notif(params[1]+" will now persist"));
	}
	if (params[0].toUpperCase()=="PERISH"){
		chatshow(notif(params[1]+" is now perishable"));
	}
	$(".out").scrollTop($(".out").scrollTop()+10000000);
}

function closeandleave(){
	if (gloflag==1){
		socket_send("/LOGOUT");
	}
}

function createfocus(elem){
	$(".tabs").html($(".tabs").html()+"<div id=\""+elem+"\" class=\"chattab active\" onclick=\"switchfocus(this.innerHTML);\">"+elem+"</div>");
	var tempactive=$(".active").html();
	$("#"+tempactive).removeClass('active');
	$("#"+tempactive).addClass('chattab');
	$(".out").html($(".out").html()+"<div class=\""+elem+"\"></div>");
	$("."+tempactive).css("display","none");
	$(".topic").html($(".topic").html()+"<div style=\"height:17px; padding:2px; border:solid 1px red;\" id=\""+elem+"topic\"> </div>")
	$("#"+elem+"topic").css("display","block");
	$("#"+tempactive+"topic").css("display","none");
}

function switchfocus(elem){
	var tempactive=$(".active").html();
	$("#"+tempactive).removeClass('active');
	$("#"+tempactive).addClass('chattab');
	$("."+tempactive).css("display","none");
	$("#"+elem).addClass('active');
	$("."+elem).css("display","inline");
	$("#"+tempactive+"topic").css("display","none");
	$("#"+elem+"topic").css("display","block");
	$(".out").scrollTop("10000000");
}

function removechan(elem){
	$("#"+elem).remove();
	$("."+elem).remove();
	var tempactive=$(".tabs div:last-child").html();
	$("#"+tempactive).addClass('active');
	$("."+tempactive).css("display","inline");
	$("#"+tempactive+"topic").css("display","block");
	$("#"+elem+"topic").remove();
}