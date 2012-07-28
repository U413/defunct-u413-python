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
	var soundManagerExists=window['soundManager']!=undefined;
	var sound;

	$.coolType={
		setup:function(options){
			var defaultSettings=$.extend({
				speed:25,
				caretChar:'\u2588',
				playSound:false,
				soundFile:null,
				volume:100,
				onSoundLoaded:null,
				insertBefore:'',
				insertAfter:'',
				delayBefore:0,
				delayAfter:0,
				style:'',
				inline:false,
				caretBlinkSpeed:300,
				scrollToBottom:false
			},options)
			$(window).data('coolTypeDefaults',defaultSettings);

			if(defaultSettings.scrollToBottom && !$.scrollTo){
				throw 'You are missing a reference to the scrollTo jQuery plugin. Visit http://plugins.jquery.com/project/ScrollTo to obtain it.';
			}

			if(!soundManagerExists && defaultSettings.soundFile){
				throw 'You are missing a reference to the sound manager script. Visit http://www.schillmania.com/projects/soundmanager2/ to obtain it.';
			}
			else if(soundManagerExists && defaultSettings.soundFile){
				LoadSound(defaultSettings.soundFile,defaultSettings.volume,defaultSettings.onSoundLoaded);
			}
		}
	}

	function LoadSound(soundFile,volume,callback){
		if(sound!=null){
			sound.destroy();
		}
		soundManager.onready(function(){
			sound=soundManager.createSound({
				id:'coolType',
				url:soundFile,
				autoLoad:true,
				stream:true,
				multishot:true,
				loops:999999999,
				volume:volume,
				onload:function(){
					callback();
				}
			});
			sound.load();
		});
	}

	$.fn.coolType=function(text,callback,options){
		var $this=this;

		var defaultSettings=$(window).data('coolTypeDefaults');
		var settings=$.extend(defaultSettings,options);

		if(settings.scrollToBottom && !$.scrollTo){
			throw 'You are missing a reference to the scrollTo jQuery plugin. Visit http://plugins.jquery.com/project/ScrollTo to obtain it.';
		}

		if(!settings.inline){
			if(settings.style!=''){
				$this.append('<div class="coolType" style="'+settings.style+'"></div>');
			}
			else{
				$this.append('<div class="coolType"></div>');
			}
		}
		else{
			if(settings.style!=''){
				$this.append('<span class="coolType" style="'+settings.style+'"></span>');
			}
			else{
				$this.append('<span class="coolType"></span>');
			}
		}

		var $container=$this.find('.coolType:last-child');
		$container.data('coolTypeText',new String());
		if(settings.style!=''){
			$container.append(settings.insertBefore+'<span style="'+settings.style+'" class="coolTypeLineContainer"></span><span id="coolTypeCaret">'+settings.caretChar+'</span>'+settings.insertAfter);
		}
		else{
			$container.append(settings.insertBefore+'<span class="coolTypeLineContainer"></span><span id="coolTypeCaret">'+settings.caretChar+'</span>'+settings.insertAfter);
		}	

		var $lineContainer=$container.find('.coolTypeLineContainer');
		var $caret=$container.find('#coolTypeCaret');

		function blinkCaret(){
			if($caret.data('Visible')){
				hideCaret();
			}
			else{
				showCaret();
			}
		}

		function showCaret(){
			$caret.data('Visible',true);
			$caret.html(settings.caretChar);
		}

		function hideCaret(){
			$caret.data('Visible',false);
			$caret.html('&nbsp;');
		}

		var blinkId=setInterval(blinkCaret,settings.caretBlinkSpeed);

		var index=0;
		setTimeout(function(){
			clearInterval(blinkId);
			showCaret();
			if(settings.playSound && sound!=null){
				sound.play({volume:settings.volume});
			}
			var intervalId=setInterval(function(){
				var char=text.substr(index,1);
				if(index!=text.length){
					var newText=$container.data('coolTypeText')+char;
					$container.data('coolTypeText',newText);
					$lineContainer.text(newText);
					if(settings.scrollToBottom){
						$this.scrollTo('100%',0,{axis:'y'});
					}
				}
				else{
					clearInterval(intervalId);
					if(settings.playSound && sound!=null){
						sound.stop();
					}
					var blinkId=setInterval(blinkCaret,settings.caretBlinkSpeed);
					setTimeout(function(){
						clearInterval(blinkId);
						$caret.remove();
						if(callback) callback($this);
					},settings.delayAfter);
				}
				index++;
			},settings.speed);
		},settings.delayBefore);
	};

	$(function(){
		$.coolType.setup();
	});
})(jQuery);
