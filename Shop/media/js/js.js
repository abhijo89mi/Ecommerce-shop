$(function(){
$('ul#header_links li').last(1).addClass('last_item');
});
$(function(){
$('#tmfooterlinks  div ul li a').hover( function(){$(this).stop().animate({paddingLeft:'0', marginLeft:'10px'},500,'easeOutSine');}, function(){$(this).stop().animate({paddingLeft:'0', marginLeft:'0px'},500,'easeInSine');});
});