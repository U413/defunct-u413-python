//   **************************************************************************
//   *                                                                        *
//   * This program is free software:you can redistribute it and/or modify    *
//   * it under the terms of the GNU General Public License as published by   *
//   * the Free Software Foundation,either version 3 of the License,or        *
//   * (at your option) any later version.                                    *
//   *                                                                        *
//   * This program is distributed in the hope that it will be useful,        *
//   * but WITHOUT ANY WARRANTY;without even the implied warranty of          *
//   * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
//   * GNU General Public License for more details.                           *
//   *                                                                        *
//   * You should have received a copy of the GNU General Public License      *
//   * along with this program.  If not,see <http://www.gnu.org/licenses/>.   *
//   *                                                                        *
//   **************************************************************************
    
(function($){
	var $terminalDisplay;
	var $notifications;
	var $loading;
	var $context;
	var $cli;
	var $commandForm;
	var $elementToScroll;
	var settings;
	var cliHistory=new Array();
	var historyIndex=0;

	function SendCommand(commandString){
		var apiUrl=$commandForm.data('apiUrl');
		$cli.data('disablePost',true);
		DisplayLoading();
		$.ajax({
			dataType:'jsonp',
			type:'post',
			data:{parseAsHtml:true,cli:commandString,session:$commandForm.data('sessionId')},
			url:apiUrl,
			success:function(apiResult){
				$commandForm.data('sessionId',apiResult.SessionId);
				ParseResult(apiResult);
			},
			error:function(xhr,ajaxOptions,thrownError){
				$terminalDisplay.append('<span style="color:#f00;">'+xhr.responseText+'</span>');
			},
			complete:function(){
				HideLoading();
			}
		});
	}

	function ParseResult(apiResult){
		$context.text(apiResult.ContextText);
		if(apiResult.PasswordField && !$cli.data('passwordField')){
			$cli.replaceWith('<input type="password" id="'+settings.cliElement.replace("#","")+'"/>');
			$cli=$(settings.cliElement);
			$cli.data('passwordField',true).focus();
		}
		else if(!apiResult.PasswordField && $cli.data('passwordField')){
			$cli.replaceWith('<textarea autocomplete="off" autofocus="autofocus" id="'+settings.cliElement.replace("#","")+'"></textarea>');
			$cli=$(settings.cliElement);
			$cli.focus().elastic();
		}
		document.title=apiResult.TerminalTitle;
		if(apiResult.ClearScreen){
			$terminalDisplay.html('');
		}
		if(apiResult.Exit){
			window.close();
		}
		if(apiResult.EditText!=null){
			$cli.val(apiResult.EditText).elastic().focus();
		}
		if(apiResult.DisplayItems.length>0){
			$terminalDisplay.append('<br/>');
			TypeLines(apiResult.DisplayItems,apiResult.ScrollToBottom);
		}
		else{
			$cli.data('disablePost',false);
		}
	}

	function TypeLines(displayItems,scrollToBottom){
		if(!$terminalDisplay.data('index')){
			$terminalDisplay.data('index',0);
		}
		var index=$terminalDisplay.data('index');
		var displayItem=displayItems[index];
		var nextLine=function(){
			index++;
			if(!(index>=displayItems.length))
			{
				$terminalDisplay.data('index',index);
				TypeLines(displayItems,scrollToBottom);
			}
			else{
				$terminalDisplay.data('index',0);
				$cli.data('disablePost',false);

				$('code').addClass('prettyprint');
				prettyPrint();
			}
		};
		if(!displayItem.DontType){
			var $lineContainer=$('<div>'+displayItem.Text+'</div>');
			var lineText=$lineContainer.text();
			if(lineText.length>0){
				if($lineContainer.attr('class')===undefined){
					$terminalDisplay.coolType(lineText,function(){
						nextLine();
					},{
						insertBefore:'<span>',
						insertAfter:'</span>',
						playSound:!displayItem.Mute
					});
				}
				else{
					$terminalDisplay.coolType(lineText,function(){
						nextLine();
					},{
						insertBefore:'<span class="'+$lineContainer.attr('class')+'">',
						insertAfter:'</span>',
						playSound:!displayItem.Mute
					});
				}
			}
			else{
				$terminalDisplay.append('<br/>');
				nextLine();
			}
		}
		else{
			$terminalDisplay.append(displayItem.Text+'<br/>');
			nextLine();
		}
		if(scrollToBottom){
			$elementToScroll.scrollTo('100%',0,{axis:'y'});
		}
		else{
			$elementToScroll.scrollTo('0%',0,{axis:'y'});
		}
	}

	function DisplayLoading(){
		if(!$loading.data('numberOfLoadings')){
			$loading.data('numberOfLoadings',0);
		}
		if($loading.data('numberOfLoadings')==0){
			$loading.show()
				.data('step',0)
				.data('intervalId',
				setInterval(function(){
					var loadingText="Loading";
					var step=$loading.data('step');
					for (count=0;count<step;count++){
						loadingText+=".";
					}
					$loading.html(loadingText);
					step++;
					if(step>10){
						step=0;
					}
					$loading.data('step',step);
				},500));
		}
		var numberOfLoadings=$loading.data('numberOfLoadings')+1;
		$loading.data('numberOfLoadings',numberOfLoadings);
	}

	function HideLoading(){
		var numberOfLoadings=$loading.data('numberOfLoadings')-1;
		$loading.data('numberOfLoadings',numberOfLoadings);
		if(numberOfLoadings==0){
			clearInterval($loading.data('intervalId'));
			$loading.data('intervalId',null);
			$loading.html('');
			$loading.hide();
		}
	}

	$.fn.extend({
		u413Client:function(options){
			$commandForm=this;

			settings=$.extend({
				terminalDisplayElement:'#terminalDisplay',
				notificationsElement:'#notifications',
				contextDisplayElement:'#context',
				loadingElement:'#loading',
				cliElement:'#Cli',
				elementToScroll:document,
				apiUrl:'http://api.u413.com/api/u413.py',
				sessionId:null
			},options);

			$terminalDisplay=$(settings.terminalDisplayElement);
			$notifications=$(settings.notificationsElement);
			$context=$(settings.contextDisplayElement);
			$cli=$(settings.cliElement);
			$loading=$(settings.loadingElement).hide();
			$elementToScroll=$(settings.elementToScroll);

			$commandForm.data('apiUrl',settings.apiUrl);

			if(settings.sessionId!=null){
				$commandForm.data('sessionId',settings.sessionId);
			}

			$('.transmit').live('click',function(e){
				$cli.focus();
				$cli.val($cli.val()+$(this).text());
			});

			var $body=$('body');

			$body.live('keydown',function(e){
				if(!$body.data('dontHandle')){
					var key=e.keyCode;
					if(!e.shiftKey && !e.altKey && !e.ctrlKey){
						$cli.data('continueKeyPress',true);
					}

					if($cli.data('hasFocus') && !$cli.data('passwordField')){
						var firstLine=$cli.val().indexOf('\n');
						var lastLine=$cli.val().lastIndexOf('\n');
						var cursor=$cli.getCursorPosition();

						if(e.shiftKey && key==13){
							$cli.insertAtCaret('\n');
							$elementToScroll.scrollTo($cli,0,{axis:'y'});
							e.preventDefault();
						}
						else if(key==38 && ((cursor<firstLine) || firstLine==-1)){
							if(historyIndex>0){
								if(historyIndex==cliHistory.length)
									$cli.data('currentValue',$cli.val());
								historyIndex--;
								$cli.val(cliHistory[historyIndex]);
								$cli.setCursorPosition(0);
							}
						}
						else if(key==40 && ((cursor>lastLine) || firstLine==-1)){
							if(historyIndex<cliHistory.length){
								historyIndex++;
								if(historyIndex==cliHistory.length)
									$cli.val($cli.data('currentValue'));
								else
									$cli.val(cliHistory[historyIndex]);
								$cli.setCursorPosition($cli.val().length);
							}
						}
					}
				}
			});

			$body.live('keypress',function(e){
				if(!$body.data('dontHandle')){
					if($cli.data('continueKeyPress')){
						var key=e.keyCode?e.keyCode:e.charCode;
						if(e.keyCode && e.charCode)
							key=e.charCode;
						if(key!=13){
							var letter=String.fromCharCode(key);
							if($cli.data('hasFocus')==false){
								$elementToScroll.scrollTo($cli,0,{axis:'y'});
								$cli.focus().val($cli.val()+letter);
								e.preventDefault();
							}
						}
						else{
							$commandForm.submit();
							e.preventDefault();
						}
					}
				}
				else{
					$body.data('dontHandle',false);
				}
			});

			$cli.live('focus',function(){
				$(this).data('hasFocus',true);
			});

			$cli.live('blur',function(){
				$(this).data('hasFocus',false);
			});

			$cli.replaceWith('<textarea autocomplete="off" autofocus="autofocus" id="'+settings.cliElement.replace("#","")+'"></textarea>');
			$cli=$(settings.cliElement);
			$cli.focus().elastic();

			$commandForm.submit(function(e){
				e.preventDefault();
				if(!$cli.data('disablePost')){
					var cliText=$cli.val();
					if(!$cli.data('passwordField'))
						cliHistory[cliHistory.length]=cliText;
					historyIndex=cliHistory.length;
					$cli.val('');
					SendCommand(cliText);
				}
			});

			SendCommand('INITIALIZE');
			
			return $commandForm;
		},

		getCursorPosition:function(){
			var pos=0;
			var input=this[0];
			// IE Support
			if(document.selection){
				input.focus();
				var sel=document.selection.createRange();
				var selLen=document.selection.createRange().text.length;
				sel.moveStart('character',-input.value.length);
				pos=sel.text.length-selLen;
			}
			// Firefox support
			else if(input.selectionStart || input.selectionStart=='0'){
				pos=input.selectionStart;
			}

			return pos;
		},

		setCursorPosition:function(pos){
			return this.each(function(){
				if(this.setSelectionRange){
					this.focus();
					this.setSelectionRange(pos,pos);
				}
				else if(this.createTextRange){
					var range=this.createTextRange();
					range.collapse(true);
					range.moveEnd('character',pos);
					range.moveStart('character',pos);
					range.select();
				}
			});
		},

		elastic:function(){
			//	  We will create a div clone of the textarea
			//	  by copying these attributes from the textarea to the div.
			var mimics=[
				'paddingTop',
				'paddingRight',
				'paddingBottom',
				'paddingLeft',
				'fontSize',
				'lineHeight',
				'fontFamily',
				'width',
				'fontWeight',
				'border-top-width',
				'border-right-width',
				'border-bottom-width',
				'border-left-width',
				'borderTopStyle',
				'borderTopColor',
				'borderRightStyle',
				'borderRightColor',
				'borderBottomStyle',
				'borderBottomColor',
				'borderLeftStyle',
				'borderLeftColor'
			];

			return this.each(function(){
				// Elastic only works on textareas
				if(this.type!=='textarea'){
					return false;
				}

				var $textarea=jQuery(this),
								$twin=jQuery('<div/>').css({
									'position':'absolute',
									'display':'none',
									'word-wrap':'break-word',
									'white-space':'pre-wrap'
								}),
								lineHeight=parseInt($textarea.css('line-height'),10) || parseInt($textarea.css('font-size'),'10'),
								minheight=parseInt($textarea.css('height'),10) || lineHeight*3,
								maxheight=parseInt($textarea.css('max-height'),10) || Number.MAX_VALUE,
								goalheight=0;

				// Opera returns max-height of -1 if not set
				if(maxheight<0){
					maxheight=Number.MAX_VALUE;}

				// Append the twin to the DOM
				// We are going to meassure the height of this,not the textarea.
				$twin.appendTo($textarea.parent());

				// Copy the essential styles (mimics) from the textarea to the twin
				var i=mimics.length;
				while (i--){
					$twin.css(mimics[i].toString(),$textarea.css(mimics[i].toString()));
				}

				// Updates the width of the twin. (solution for textareas with widths in percent)
				function setTwinWidth(){
					var curatedWidth=Math.floor(parseInt($textarea.width(),10));
					if($twin.width()!==curatedWidth){
						$twin.css({'width':curatedWidth+'px'});

						// Update height of textarea
						update(true);
					}
				}

				// Sets a given height and overflow state on the textarea
				function setHeightAndOverflow(height,overflow){
					var curratedHeight=Math.floor(parseInt(height,10));
					if($textarea.height()!==curratedHeight){
						$textarea.css({'height':curratedHeight+'px','overflow':overflow});
					}
				}

				// This function will update the height of the textarea if necessary 
				function update(forced){
					// Get curated content from the textarea.
					var textareaContent=$textarea.val().replace(/&/g,'&amp;').replace(/ {2}/g,'&nbsp;').replace(/<|>/g,'&gt;').replace(/\n/g,'<br/>');

					// Compare curated content with curated twin.
					var twinContent=$twin.html().replace(/<br>/ig,'<br/>');

					if(forced || textareaContent+'&nbsp;'!==twinContent){

						// Add an extra white space so new rows are added when you are at the end of a row.
						$twin.html(textareaContent+'&nbsp;');

						// Change textarea height if twin plus the height of one line differs more than 3 pixel from textarea height
						if(Math.abs($twin.height()+lineHeight-$textarea.height())>3){

							var goalheight=$twin.height()+lineHeight;
							if(goalheight>=maxheight){
								setHeightAndOverflow(maxheight,'auto');
							}
							else if(goalheight<=minheight){
								setHeightAndOverflow(minheight,'hidden');
							}
							else{
								setHeightAndOverflow(goalheight,'hidden');
							}
						}
					}
				}

				// Hide scrollbars
				$textarea.css({'overflow':'hidden'});

				// Update textarea size on keyup,change,cut and paste
				$textarea.bind('keyup change cut paste',function(){
					update();
				});

				// Update width of twin if browser or textarea is resized (solution for textareas with widths in percent)
				$(window).bind('resize',setTwinWidth);
				$textarea.bind('resize',setTwinWidth);
				$textarea.bind('update',update);

				// Compact textarea on blur
				$textarea.bind('blur',function(){
					if($twin.height()<maxheight){
						if($twin.height()>minheight){
							$textarea.height($twin.height());
						}
						else{
							$textarea.height(minheight);
						}
					}
				});

				// And this line is to catch the browser paste event
				$textarea.bind('input paste',function(e) {setTimeout(update,250);});

				// Run update once when elastic is initialized
				update();
			});
		},

		insertAtCaret:function(myValue){
			return this.each(function(i){
				if(document.selection){
					this.focus();
					sel=document.selection.createRange();
					sel.text=myValue;
					this.focus();
				}
				else if(this.selectionStart || this.selectionStart=='0'){
					var startPos=this.selectionStart;
					var endPos=this.selectionEnd;
					var scrollTop=this.scrollTop;
					this.value=this.value.substring(0,startPos)+myValue+this.value.substring(endPos,this.value.length);
					this.focus();
					this.selectionStart=startPos+myValue.length;
					this.selectionEnd=startPos+myValue.length;
					this.scrollTop=scrollTop;
				}
				else{
					this.value+=myValue;
					this.focus();
				}
			});
		}
	});
})(jQuery);
