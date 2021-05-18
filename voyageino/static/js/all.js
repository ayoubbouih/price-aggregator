/*-------------------------------------------------------------------------------------------------------------------------------*/
/*This is main JS file that contains custom style rules used in this template*/
/*-------------------------------------------------------------------------------------------------------------------------------*/
/* Template Name: Travel*/
/* Version: 1.0 Initial Release*/
/* Build Date: 22-04-2015*/
/* Author: Unbranded*/
/* Website: http://moonart.net.ua/site/ 
/* Copyright: (C) 2015 */
/*-------------------------------------------------------------------------------------------------------------------------------*/

/*--------------------------------------------------------*/
/* TABLE OF CONTENTS: */
/*--------------------------------------------------------*/
/* 01 - VARIABLES */
/* 02 - PAGE CALCULATIONS */
/* 03 - FUNCTION ON DOCUMENT READY */
/* 04 - FUNCTION ON PAGE LOAD */
/* 05 - FUNCTION ON PAGE RESIZE */
/* 06 - FUNCTION ON PAGE SCROLL */
/* 07 - SWIPER SLIDERS */
/* 08 - BUTTONS, CLICKS, HOVERS */
/* 09 - LIGHT-BOX */

/*-------------------------------------------------------------------------------------------------------------------------------*/
$(function() {

	"use strict";
	
	
    
	/*================*/
	/* 01 - VARIABLES */
	/*================*/
	
	var swipers = [], winW, winH, winScr, $container, _isresponsive, xsPoint = 451, smPoint = 768, mdPoint = 992, lgPoint = 1200, addPoint = 1600, _ismobile = navigator.userAgent.match(/Android/i) || navigator.userAgent.match(/webOS/i) || navigator.userAgent.match(/iPhone/i) || navigator.userAgent.match(/iPad/i) || navigator.userAgent.match(/iPod/i);

	/*========================*/
	/* 02 - PAGE CALCULATIONS */
	/*========================*/
	function pageCalculations(){
		winW = $(window).width();
		winH = $(window).height();
		if($('.menu-button').is(':visible')) _isresponsive = true;
		else _isresponsive = false;		
	}

	/*=================================*/
	/* 03 - FUNCTION ON DOCUMENT READY */
	/*=================================*/
	pageCalculations();
	accordionChooser();

	//center all images inside containers
	$('.center-image').each(function(){
		var bgSrc = $(this).attr('src');
		$(this).parent().addClass('background-block').css({'background-image':'url('+bgSrc+')'});
		$(this).hide();
	});
	$('.center-image-op').each(function(){
		var bgSrc = $(this).attr('src');
		$(this).parent().addClass('background-block-op').css({'background-image':'linear-gradient(rgba(0,0,0,0.2),rgba(0,0,0,0.2)),url('+bgSrc+')'});
		$(this).hide();
	});
	$('.center-image-index').each(function(){
		var bgSrc = $(this).attr('src');
		$(this).parent().addClass('background-block-op').css({'background-image':'linear-gradient(rgba(255,102,0,0.2),rgba(255,102,0,1))'});
		$(this).hide();
	});
	//sticked header
	var $st_header = $('header');
	if($st_header.hasClass('header-sticked')){
		if ($st_header.hasClass('st-58')){
			$('body').addClass('st-58');
		} else if ($st_header.hasClass('st-100')){
			$('body').addClass('st-100');
		} else if($st_header.hasClass('st-148')){
			$('body').addClass('st-148');
		} else{			
			$('body').addClass('stick');
		}
		
	}			
	
	/*============================*/
	/* 04 - FUNCTION ON PAGE LOAD */
	/*============================*/
	$(window).load(function(){
		initFullPage();		
		initSwiper();
		videoRezise();
		tpEntryHover();
		$('.loading').fadeOut(700);

		$('.isotope-container').isotope({itemSelector: '.item', masonry:{gutter:0,columnWidth:'.grid-sizer'}});
		var initValue = $('.filter-nav').find('.selected a').attr('data-filter');
		$container.isotope({itemSelector: '.item', filter: initValue,masonry:{gutter:0,columnWidth:'.grid-sizer'}});
		


	});
	/*==============================*/
	/* 05 - FUNCTION ON PAGE RESIZE */
	/*==============================*/
	function resizeCall(){
		pageCalculations();
		videoRezise();
		initFullPage();
		updateFullPage();
		tpEntryHover();

		$('.swiper-container.initialized[data-slides-per-view="responsive"]').each(function(){
			var thisSwiper = swipers['swiper-'+$(this).attr('id')], $t = $(this), slidesPerViewVar = updateSlidesPerView($t);
			thisSwiper.params.slidesPerView = slidesPerViewVar;
			thisSwiper.reInit();
			var paginationSpan = $t.find('.pagination span');
			var paginationSlice = paginationSpan.hide().slice(0,(paginationSpan.length+1-slidesPerViewVar));
			if(paginationSlice.length<=1 || slidesPerViewVar>=$t.find('.swiper-slide').length) $t.addClass('pagination-hidden');
			else $t.removeClass('pagination-hidden');
			paginationSlice.show();
		});
	}
	if(!_ismobile){
		$(window).resize(function(){
			resizeCall();
		});
	} else{
		window.addEventListener("orientationchange", function() {
			resizeCall();
		}, false);
	}

	/*=====================*/
	/* 07 - swiper sliders */
	/*=====================*/
	function initSwiper(){
		var initIterator = 0;
		$('.swiper-container').each(function(){								  
			var $t = $(this);								  

			var index = 'swiper-unique-id-'+initIterator;

			$t.addClass('swiper-'+index + ' initialized').attr('id', index);
			$t.find('.pagination').addClass('pagination-'+index);

			var autoPlayVar = parseInt($t.attr('data-autoplay'),10);
			var centerVar = parseInt($t.attr('data-center'),10);
			var simVar = ($t.closest('.circle-description-slide-box').length)?false:true;

			var slidesPerViewVar = $t.attr('data-slides-per-view');
			if(slidesPerViewVar == 'responsive'){
				slidesPerViewVar = updateSlidesPerView($t);
			}
			else slidesPerViewVar = parseInt(slidesPerViewVar,10);

			var loopVar = parseInt($t.attr('data-loop'),10);
			var speedVar = parseInt($t.attr('data-speed'),10);

			var slidesPerGroup = parseInt($t.attr('data-slides-per-group'),10);
			if(!slidesPerGroup){slidesPerGroup=1;}			

			swipers['swiper-'+index] = new Swiper('.swiper-'+index,{
				speed: speedVar,
				pagination: '.pagination-'+index,
				loop: loopVar,
				paginationClickable: true,
				autoplay: autoPlayVar,
				slidesPerView: slidesPerViewVar,
				slidesPerGroup: slidesPerGroup,
				keyboardControl: true,
				calculateHeight: true, 
				simulateTouch: simVar,
				centeredSlides: centerVar,
				roundLengths: true,
				onInit: function(swiper){
					var browserWidthResize = $(window).width();
					if (browserWidthResize < 750) {
							swiper.params.slidesPerGroup=1;
					} else { 
                      swiper.params.slidesPerGroup=slidesPerGroup;
					}
				},
				onResize: function(swiper){
					var browserWidthResize2 = $(window).width();
					if (browserWidthResize2 < 750) {
							swiper.params.slidesPerGroup=1;
					} else { 
                      swiper.params.slidesPerGroup=slidesPerGroup;
					  swiper.resizeFix(true);
					}					
				},									
				onSlideChangeEnd: function(swiper){
					var activeIndex = (loopVar===1)?swiper.activeLoopIndex:swiper.activeIndex;
					var qVal = $t.find('.swiper-slide-active').attr('data-val');
					$t.find('.swiper-slide[data-val="'+qVal+'"]').addClass('active');
				},
				onSlideChangeStart: function(swiper){
					$t.find('.swiper-slide.active').removeClass('active');
					if($t.hasClass('thumbnails-preview')){
						var activeIndex = (loopVar===1)?swiper.activeLoopIndex:swiper.activeIndex;
						swipers['swiper-'+$t.next().attr('id')].swipeTo(activeIndex);
						$t.next().find('.current').removeClass('current');
						$t.next().find('.swiper-slide[data-val="'+activeIndex+'"]').addClass('current');
					}
				},
				onSlideClick: function(swiper){
					if($t.hasClass('thumbnails')) {
						swipers['swiper-'+$t.prev().attr('id')].swipeTo(swiper.clickedSlideIndex);
					}
				}
			});
			swipers['swiper-'+index].reInit();
			if($t.attr('data-slides-per-view')=='responsive'){
				var paginationSpan = $t.find('.pagination span');
				var paginationSlice = paginationSpan.hide().slice(0,(paginationSpan.length+1-slidesPerViewVar));
				if(paginationSlice.length<=1 || slidesPerViewVar>=$t.find('.swiper-slide').length) $t.addClass('pagination-hidden');
				else $t.removeClass('pagination-hidden');
				paginationSlice.show();
			}
			initIterator++;
		});

	}

	function updateSlidesPerView(swiperContainer){
		if(winW>=addPoint) return parseInt(swiperContainer.attr('data-add-slides'),10);
		else if(winW>=lgPoint) return parseInt(swiperContainer.attr('data-lg-slides'),10);
		else if(winW>=mdPoint) return parseInt(swiperContainer.attr('data-md-slides'),10);
		else if(winW>=smPoint) return parseInt(swiperContainer.attr('data-sm-slides'),10);
		else if(winW>=xsPoint) return parseInt(swiperContainer.attr('data-xs-slides'),10);
		else return parseInt(swiperContainer.attr('data-mob-slides'),10);
	}

	//swiper arrows
	$('.swiper-arrow-left').on('click',function(){
		swipers['swiper-'+$(this).closest('.arrows').find('.swiper-container').attr('id')].swipePrev();
	});
	$('.swiper-arrow-right').on('click',function(){
		swipers['swiper-'+$(this).closest('.arrows').find('.swiper-container').attr('id')].swipeNext();
	});


	
	/*==============================*/
	/* 06 - FUNCTION ON PAGE SCROLL */
	/*==============================*/	
	$(window).scroll(function() {
	    if ($(window).scrollTop() >= 10){
			$('header').addClass('scrol');
		}else {
			$('header').removeClass('scrol');
		}
		
		
	});
	
	if ($(window).width()<768){
		
		$('.drop-tabs').on( "click", function() {
			if($('.arrow-down').hasClass('act')){
				$(this).find('.arrow-down').removeClass('act');
				$(this).find('.nav-tabs').slideUp(400);
				
			}else{
               	$('.drop span').slideUp(300);
				$(this).find('.arrow-down').addClass('act');
				$(this).find('.nav-tabs').slideDown(400);
			}
			return false;
		});
		
		
		
		
    	$('.click-tabs').on( "click", function() {
			var tabbIndex =$(this).index();
			$(this).parent().parent().parent().find('b').text($(this).text());
			$('.drop-tabs').find('.nav-tabs').slideUp(400);
		    $('.tab-pane').removeClass('active');
		    $('.tab-pane').eq(tabbIndex).addClass('active');
		});
	}
	
	
		
		function timePiker() {
			$('.timePiker').each(function(){
			   $('.timePiker').DateTimePicker({
					dateTimeFormat: "dd-MM-yyyy hh:mm:ss AA",
					maxDateTime: "20-07-2016 12:00:00 AM",
					minDateTime: "20-07-2012 12:00:00 AM",


					animationDuration: 100
				});
			});
		    
		 }
	
	timePiker();
	
	$('.click-tabs a').on('click', function(){
		timePiker();
		});
	
	/***********************************/
	/*VIDEO CKICK*/
	/**********************************/
				 
	$('.video-click').on( "click", function() {
			$(this).find('iframe').attr('src',$(this).find('.video-change').attr('href') + '&autoplay=1');
            $(this).find('.video').show();
            $(this).find('.img-href').hide();
			$(this).find('.video-title').hide();
	    });
				   
		$('.video .close-v').on('click', function(){
			$('.video').fadeOut(500, function(){
				$('.video iframe').attr('src','');
				$('.img-href').show();
				$('.video-title').show();
			});
	});
	function videoRezise(){
		$('.video-click').find('iframe').height($('.img-href').height());
	}

    $(document).on('click', '.video-open', function(){
		$('.video-player').addClass('active');
		var videoSource = $(this).find('img').attr('data-src');
		setTimeout(function(){$('.video-player iframe').attr('src', videoSource);}, 1000);
	});

	$('.video-player .close-iframe').on('click', function(){
		$('.video-player iframe').attr('src', '');
		setTimeout(function(){$('.video-player').removeClass('active');}, 1000);
		
	});

	$('#fullpage').on('mousewheel', function(event) {
    	console.log(event.deltaX, event.deltaY, event.deltaFactor);
	});

	/*==============================*/
	/* 06 - POPUPS */
	/*==============================*/
	//search popup
	
	$('.search .search-img').on( "click", function() {
		$(this).siblings('.search-popup').toggleClass("active");
		return false;
	});
	$('.s_close	').on( "click", function() {
		$(this).parent('.search-popup').toggleClass("active");
		return false;
	});	


	//cart popup
	$('.card-icon, .card-link').on( "click", function() {
		$(this).siblings('.cart-popup').slideToggle();
		return false;
	});
	$('.cart_close').on( "click", function() {
		$(this).parent('.cart-popup').slideToggle();
		return false;
	});	
	$('.cart-popup .item-remove').on( "click", function() {
		$(this).parents('.hotel-small').remove();
		return false;
	});	


	/*==============================*/
	/* 06 - TABS, DROPDOWNS, COUNTERS, DATEPIKER  */
	/*==============================*/
	
    //Tabs
	var tabFinish = 0;
	$(document).on('click', '.nav-tab-item', function(){
		
	    var $t = $(this);
	    if(tabFinish || $t.hasClass('active')) return false;
	    tabFinish = 1;
	    $t.closest('.nav-tab').find('.nav-tab-item').removeClass('active');
	    $t.addClass('active');
	    var index = $t.parent().parent().find('.nav-tab-item').index(this);
	    $t.closest('.tab-wrapper').find('.tab-info:visible').fadeOut(500, function(){
	        $t.closest('.tab-wrapper').find('.tab-info').eq(index).fadeIn(500, function() {
	            tabFinish = 0;
	            resizeCall();
				setTimeout (function(){
				  initSwiper();
				},500)
				
	        });
	    });
	});

	$('.cat-drop').on('click', function(){
		var $t = $(this).parent('li');
		if ($t.hasClass('active')) return false;
		/*$t.parent('.sidebar-category').find('li.active ul').slideToggle(300, function(){
			$(this).parent('li').removeClass('active');
			 $t.addClass('active').find('ul').slideToggle(300);
		});*/
		var $cat_active = $t.parent('.sidebar-category').find('li.active');
		$cat_active.removeClass('active');
		$cat_active.find('ul').slideToggle();
		$t.addClass('active').find('ul').slideToggle();

		return false;
	});

	//Dropdown
	$('.drop').on( "click", function() {
		if($(this).find('.drop-list').hasClass('act')){
			$(this).find('.drop-list').removeClass('act');
			$(this).find('span').slideUp(300);
		}else{
           	$('.drop span').slideUp(300);
           	$('.drop .act').removeClass('act');
			$(this).find('.drop-list').addClass('act');
			$(this).find('span').slideDown(300);
		}
		return false;
	});
    $('.drop span a').on( "click", function() {
			$(this).parent().parent().find('b').text($(this).text());
			$('.drop').find('span').slideUp(300);
	});

	/*accordion*/
	$('.accordion').each(function(){
		$(this).find('.acc-title').on("click", function(){
			if($(this).hasClass('active')){
				$(this).removeClass('active');
				$(this).siblings('.acc-body').slideUp();
			} else{
				$(this).closest('.accordion').find('.active').removeClass('active');
				$(this).closest('.accordion').find('.acc-body').slideUp('slow');
				$(this).toggleClass('active');
				$(this).siblings('.acc-body').slideToggle('slow');
			}
		});
	});

	//accordion-chooser
	$('.accordion-chooser a').on('click', function(){
		if($(this).hasClass('active')) return false;
		var filter = $(this).data('fifter');

		var accordion = $(this).parents('.accordion-filter').find('.accordion');
		$(this).siblings('.active').removeClass('active');		
		$(this).addClass('active');
		if (filter=="*"){
			accordion.find('.acc-panel').show();
		} else{
			accordion.find('.acc-panel:not('+filter+')').hide();			
			accordion.find(filter).show();			
		}		

		return false;
	});
	function accordionChooser(){
		if($('.accordion-chooser').length){
			var active_filter = $('.accordion-chooser').find('a.active');
			var filter = active_filter.data('fifter');
			var accordion = active_filter.parents('.accordion-filter').find('.accordion');
			active_filter.siblings('.active').removeClass('active');		
			active_filter.addClass('active');
			if (filter=="*"){
				accordion.find('.acc-panel').show();
			} else{
				accordion.find('.acc-panel:not('+filter+')').hide();			
				accordion.find(filter).show();			
			}		

			return false;			

		}
	}

	//counters
	if ($('.counters').length){
	$('.counters').viewportChecker({
		classToAdd: 'counted',
		offset: 100,
		callbackFunction: function(elem, action){
			elem.find('.counter-number').countTo();		
		}		
	});
	}

	//Datepiker	
	
    $(".to_date").datepicker({
		dateFormat: "mm/dd/yy",
		minDate:new Date($(".to_date").first().attr("min")),
	});
	$(".from_date").datepicker({
		dateFormat: "mm/dd/yy",
		minDate:new Date(),
		maxDate: new Date($(".to_date").first().attr("value")),
	});

	$(".datepicker").change(function(){
		$('.from_date').datepicker('option', 'maxDate', $(".to_date").first().val());
		$('.to_date').datepicker('option', 'minDate', $(".from_date").first().val());
		console.log("changed");
		});

	//slider range
  	$(".slider-range" ).each(function(index) {
     	var counter = $(this).data('counter');
     	var position = $(this).data('position');
     	var from = parseInt($(this).data('from'),10);
     	var to = parseInt($(this).data('to'),10);     	     	
     	var min = parseInt($(this).data('min'),10);     	     	
     	var max = parseInt($(this).data('max'),10);     	     	
     	$(this).find(".range").attr("id","slider-range-"+index);
     	$(this).find(".amount-start").attr("id","amount-start-"+index);
     	$(this).find(".amount-end").attr("id","amount-end-"+index);
	  	$("#slider-range-"+index).slider({
			range: true,
			min: min,
			max: max,
			values: [ from , to ],
			slide: function( event, ui ) {
				if (position=="start"){
					$("#amount-start-"+index).val(counter + ui.values[ 0 ]);
					$("#amount-end-"+index).val(counter + ui.values[ 1 ]);
				} else{
					$("#amount-start-"+index).val(ui.values[ 0 ] + counter);
					$("#amount-end-"+index).val(ui.values[ 1 ] + counter);					
				}
			}
	    });
	    if (position=="start"){
    		$("#amount-start-"+index).val(counter + $("#slider-range-"+index).slider("values",0));
    		$("#amount-end-"+index).val(counter + $("#slider-range-"+index).slider("values",1));
    	} else {
    		$("#amount-start-"+index).val($("#slider-range-"+index).slider("values",0) + counter);
    		$("#amount-end-"+index).val($("#slider-range-"+index).slider("values",1) + counter);    		
    	}
    });


	//circliful
	if ($('.circle-wrapper').length){
	$('.circle-wrapper').viewportChecker({
		classToAdd: 'counted',
		offset: 100,
		callbackFunction: function(elem, action){
			elem.find('.circle').circliful();
		}
	});
	}

	//progress bar
	if ($('.progress-wrapper').length){
	$('.progress-wrapper').viewportChecker({
		classToAdd: 'counted',
		offset: 100,
		callbackFunction: function(elem, action){
			elem.find('.count').countTo();
			
			elem.find('.progress-block').not('.counted').each(function(){
				$(this).addClass('counted');
				var $progress_bar = $(this).find('.progress-bar');
				var speed = parseInt($progress_bar.attr("data-speed"),10);
				var to = $progress_bar.attr("data-to");			
				$progress_bar.animate({width: to+"%"}, {duration: speed});					
			});			
		}		
	});
	}

    			
	//isotope filter
	$container = $('.filter-content');
	$('.filter-nav').on( 'click', 'a', function() {
		var filterValue = $(this).attr('data-filter');
		$container.isotope({ filter: filterValue });
		var $buttonGroup = $(this).parent().parent();
		$buttonGroup.find('.selected').removeClass('selected');
		$(this).parent().addClass('selected');
	});

	//timer
  	function format(number){
    	if(number===0){
      		return '00';
    	}else if (number < 10) {
          	return '0' + number;
      	} else{
          	return ''+number;
      	}
    }	
	function setTimer(final_date){         
		var today = new Date();
		var finalTime = new Date(final_date);
		var interval = finalTime - today;
		if(interval<0) interval = 0;
		var days = parseInt(interval/(1000*60*60*24),10);
		var daysLeft = interval%(1000*60*60*24);
		var hours = parseInt(daysLeft/(1000*60*60),10);
		var hoursLeft = daysLeft%(1000*60*60);
		var minutes = parseInt(hoursLeft/(1000*60),10);
		var minutesLeft = hoursLeft%(1000*60);
		var seconds = parseInt(minutesLeft/(1000),10);
		$('.days').text(format(days));
		$('.hours').text(format(hours));
		$('.minutes').text(format(minutes));
		$('.seconds').text(format(seconds));
	}
	if($('.back-counter').length){
	 	var final_date  = $('.back-counter').data('finaldate');
		setTimer(final_date);
		setInterval(function(){setTimer(final_date);}, 1000);	 	
	}

	//countdown
	if($('.ClassyCountdown').length){
		$('#countdown').ClassyCountdown({
			theme: "white", // theme
			end: $.now() + 645600,
			// custom style for the countdown
			style: {
			  element: '',
			  labels: false,
			  days: {gauge: {thickness: 0.05}},
			  hours: {gauge: {thickness: 0.05}},
			  minutes: {gauge: {thickness: 0.05}},
			  seconds: {gauge: {thickness: 0.05}}
			}		
		});
	}
	

	/*==============================*/
	/* 06 - CHANGE CONTENT */
	/*==============================*/
	//change hotel content simulate
    $('.choose-hotel .drop span a').on( "click", function() {
		var $hotelCont = $(this).parents(".main-wraper");
		var $hotelBg = $hotelCont.find('.hotel-clip .bg');
		var bgImg = $hotelBg.css('background-image');
		if(bgImg.match("hotel_bg.jpg")) {

			$hotelBg.fadeTo(800, 0, function()
			{
			    $(this).css({'background-image': bgImg.replace('hotel_bg.jpg','hotel_bg2.jpg')});
			}).fadeTo(800, 1);
			//$hotelBg.stop().css('background-image', bgImg.replace('hotel_bg.jpg','hotel_bg2.jpg'));

			$hotelCont.find('.hotel-choose:not(.hotel-hidden)').hide(0);
			$hotelCont.find('.hotel-choose.hotel-hidden').show(0, function() {resizeCall();});
		} else{

			$hotelBg.fadeTo(800, 0, function()
			{
			    $(this).css({'background-image': bgImg.replace('hotel_bg2.jpg','hotel_bg.jpg')});
			}).fadeTo(800, 1);
			//$hotelBg.stop().css('background-image', bgImg.replace('hotel_bg2.jpg','hotel_bg.jpg'));
			$hotelCont.find('.hotel-choose.hotel-hidden').hide(0);  			
			$hotelCont.find('.hotel-choose:not(.hotel-hidden)').show(0, function() {resizeCall();});
			
		}
	});  

	//change slider
	$('.change-slider').on( "click", function() {
		var img = $(this).attr("href");
		$(this).parents('.section').find('.bg-bg-chrome').fadeTo('slow', 0.3, function()
		{
		    $(this).css({'background-image':'url('+img+')'});
		}).fadeTo('slow', 1);
		$(this).parents('.section').find('.change-slider.active').removeClass('active');
		$(this).addClass('active');
		return false;
	});

	//left slider change
	$(document).on('click', '.slide-preview a', function(){
		var img = $(this).attr("href");
		$(this).parents('.slider-block-right').siblings('.slider-block-left').fadeTo('slow', 0.3, function()
		{
		    $(this).css({'background-image':'url('+img+')'});
		}).fadeTo('slow', 1);
		$(this).siblings('.active').removeClass('active');
		$(this).addClass('active');
		return false;
	});	

	//tab-tour-block
	var tourFinish = 0;
	$('.tab-tour-header .tab-tour').on( "click", function() {
		var $t = $(this);
		if(tourFinish || $t.hasClass('active')) return false;

		tourFinish = 1;
		var index = $t.index();
		var $c_content = $t.parents('.tab-tour-header').siblings('.tab-tour-content');

		$t.siblings('.active').removeClass('active');
		$t.addClass('active');

		$c_content.find('.hotel-wrpp.active').fadeOut(800, function(){
			$(this).removeClass('active');
	        $c_content.find('.hotel-wrpp').eq(index).fadeIn(800, function() {$(this).addClass('active');tourFinish = 0;resizeCall();});
	    });
	});
	$('.tab-select .drop span a').on( "click", function() {
		var $t = $(this);
		var index = $t.index();
		var $c_content = $t.parents('.tab-select').siblings('.tab-tour-content');
		$c_content.find('.hotel-wrpp.active').fadeOut(800, function(){
			$(this).removeClass('active');
	        $c_content.find('.hotel-wrpp').eq(index).fadeIn(800, function() {$(this).addClass('active');tourFinish = 0;resizeCall();});
	    });		
	});

    //list-grid change
    $('.change-list').on( "click", function() {
    	if ($(this).hasClass('active')) return false;
    	$(this).siblings('.active').removeClass('active');
    	$(this).addClass('active').parents('.list-header').siblings('.grid-content').removeClass('grid-content').addClass('list-content');
    });
    $('.change-grid').on( "click", function() {
    	if ($(this).hasClass('active')) return false;
    	$(this).siblings('.active').removeClass('active');    	
    	$(this).addClass('active').parents('.list-header').siblings('.list-content').removeClass('list-content').addClass('grid-content');
    });  						

	/*==============================*/
	/* 06 - FULL PAGE */
	/*==============================*/
	function initFullPage(){
		if($('.fullpage').length){
			if (winW<992) return false;
			$('body').css("overflow-y", "hidden");
			$('.fullpage').css("height", winH+"px");
			$('html, body').scrollTop(0);
		}
	}
	function updateFullPage(){
		if(!$('.fullpage').length) return false;
		if (winW>=992){
			var $wrapper = $('.fullpage-wrapper');
			var $pageActive = $('.fullpage .section.active');
			var index = $pageActive.index();
			var footer_hieght = $('.footer').outerHeight();
			if ($pageActive.hasClass('footer')){
				$wrapper.css('top', '-' +(winH*(index-1)+footer_hieght)+'px');
			} else {
				$wrapper.css('top', '-' +winH*(index)+'px');
			}
			
			$('html, body').scrollTop(0);
			//alert(count+'/'+index+'/'+winH);
		} else{
			$('body').css("overflow-y", "auto");
		}

	}	
     
	if ($('.fullpage').length){
	var fullpage = 1;
	$('.fullpage').mousewheel(function(event) {
		if (fullpage === 0) return false;
		if(winW<=991) return false;
		fullpage = 0;

		var $wrapper = $('.fullpage-wrapper');
		var $pageActive = $('.fullpage .section.active');
		var index = $pageActive.index();
		var footer_hieght = $('.footer').outerHeight();

		if(event.deltaY==-1){
			if(!$pageActive.hasClass('footer')){
				if ($pageActive.next().hasClass('footer')){
					$pageActive.removeClass('active').next().addClass('active');
					var count = (winH*(index))+footer_hieght;
					//$wrapper.css('top', '-' +count+'px');
					$wrapper.animate({top:'-'+count+'px'}, "slow", function(){fullpage=1;});	
				} else{
					$pageActive.removeClass('active').next().addClass('active');
					$wrapper.animate({top:'-'+winH*(index+1) +'px'}, "slow", function(){fullpage=1;});
					//$wrapper.css('top', '-'+winH*(index+1) +'px');					
				}
			} else{fullpage=1;}
		} else if(event.deltaY==1){
			if(index!==0){
				$pageActive.prev().addClass('active');
				$pageActive.removeClass('active');
				$wrapper.animate({top:'-'+winH*(index-1) +'px'}, "slow", function(){fullpage=1;});				
				//$wrapper.css('top', '-'+winH*(index-1) +'px');
			} else{
				fullpage=1;
			}
		}
	});		
    }
	
	$('.serach-item').on('mouseover', function(){
	   $('.serach-item input').addClass('active');
		return false;
	});
	
	$('.serach-item input').focus(function() {
	   $(this).addClass('active');
		return false;
	});
	
	$('.serach-item input').blur(function() {
	   $(this).removeClass('active');
		return false;
	});
	
	/*==============================*/
	/* 06 - MENU */
	/*==============================*/
	$('nav.menu .fa-angle-down, nav.menu .fa-chevron-right').on( "click", function() {
		$(this).parent('a').parent('li').toggleClass('active');
		$(this).parent('a').next('.dropmenu').slideToggle();
		return false;
	});

	$('.nav-menu-icon a').on('click', function() {
	  if ($('nav').hasClass('slide-menu')){
			$('nav').removeClass('slide-menu'); 
			$(this).removeClass('active');
			$('body').toggleClass('menu_opened');
	  }else {
  			$('nav').addClass('slide-menu');
		  	$(this).addClass('active');
		  	$('body').toggleClass('menu_opened');
	  }
		return false;
	 });
	
	/***********************************/
	/*STYLE BAR*/
	/**********************************/
	
	$('.conf-button').on('click', function(){
		if ($('.style-page').hasClass('slide-right')){
		    $('.style-page').removeClass('slide-right'); 
			$('.conf-button span').removeClass('act');
		}else{
		    $('.style-page').addClass('slide-right');
			$('.conf-button span').addClass('act');
		}return false;			 
    });
	
	 $('.entry').on('click', function(){
		  var prevTheme = $('body').attr('data-color');
		  var newTheme = $(this).attr('data-color');
		  if($(this).hasClass('active')) return false;
		  $(this).parent().find('.active').removeClass('active');
		  $(this).addClass('active');
		  $('body').attr('data-color', newTheme);
		  $('img').each(function() {
		   $(this).attr("src", $(this).attr("src").replace(prevTheme+'/', newTheme+'/'));
		  });
		  
	         localStorage.setItem("color", newTheme);
	 });

	var localStorageThemeVar = localStorage.getItem('color');
	$('.entry[data-color="'+localStorageThemeVar+'"]').on('click');
	
	
	$('.rounded').on('click', function() {
	   if($('body').hasClass('noborder')) {  
	    $('body').removeClass('noborder');
		 $(this).closest('.color-block').find('.check-option').removeClass('active');		
	     $(this).parent().addClass('active');
	   }
	});
    $('.norounded').on('click', function() {
	    $('body').addClass('noborder');
		$(this).closest('.color-block').find('.check-option').removeClass('active');		
	     $(this).parent().addClass('active');
	});
	
	$('.boxed').on('click', function() {
	   if($('.container').hasClass('box')) {
	    $('.container').removeClass('box');
		   $(this).closest('.color-block').find('.check-option').removeClass('active');	
	       $(this).parent().addClass('active');
		   initSwiper();
	   }
	});
    $('.noboxed').on('click', function() {
	    $('.container').addClass('box');
		$(this).closest('.color-block').find('.check-option').removeClass('active');	
	     $(this).parent().addClass('active');
		   initSwiper();
	});
	
	
    $('.accordeon-entry h5').on('click', function(){
		$(this).parent().toggleClass('active');
		$(this).next().toggleClass('active');
	});
	
	$('.alert .fa').on('click', function(){
	   $(this).parent().addClass('act');
	});
	
	/***********************************/
	/*POPUP*/
	/**********************************/
	
	if ($('.popup-gallery').length) {
		$('.popup-gallery').magnificPopup({
			delegate: 'a',
			type: 'image',
			removalDelay: 300,
			tLoading: 'Loading image #%curr%...',
			mainClass: 'mfp-fade',
			gallery: {
				enabled: true,
				navigateByImgClick: true,
				preload: [0,1] 
			},
			zoom: {
				enabled: true,
				duration: 300, 
				easing: 'ease-in-out',
				opener: function(openerElement) {
				  return openerElement.is('img') ? openerElement : openerElement.find('img');
				}
			}
		});
	}

	/***********************************/
	/*TP ENTRY*/
	/**********************************/
	function tpEntryHover() {			
		$('.top-preview .tp_entry').on('click', function() {
			if ($(window).width() <= 1024)  {
				$('.tp_entry').removeClass('tp_entry-active');
				$(this).addClass('tp_entry-active');
			} else {
				$('.tp_entry').removeClass('tp_entry-active');
			}
		});
	};
	
});
function autocomplete(inp, arr) {
	/*the autocomplete function takes two arguments,
	the text field element and an array of possible autocompleted values:*/
	var currentFocus;
	/*execute a function when someone writes in the text field:*/
	inp.addEventListener("input", function(e) {
		var a, b, i, val = this.value;
		/*close any already open lists of autocompleted values*/
		closeAllLists();
		if (!val) { return false;}
		currentFocus = -1;
		/*create a DIV element that will contain the items (values):*/
		a = document.createElement("DIV");
		a.setAttribute("id", this.id + "autocomplete-list");
		a.setAttribute("class", "autocomplete-items");
		/*append the DIV element as a child of the autocomplete container:*/
		this.parentNode.appendChild(a);
		/*for each item in the array...*/
		for (i = 0; i < arr.length; i++) {
		  /*check if the item starts with the same letters as the text field value:*/
		  if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
			/*create a DIV element for each matching element:*/
			b = document.createElement("DIV");
			/*make the matching letters bold:*/
			b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
			b.innerHTML += arr[i].substr(val.length);
			/*insert a input field that will hold the current array item's value:*/
			b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
			/*execute a function when someone clicks on the item value (DIV element):*/
			b.addEventListener("click", function(e) {
				/*insert the value for the autocomplete text field:*/
				inp.value = this.getElementsByTagName("input")[0].value;
				/*close the list of autocompleted values,
				(or any other open lists of autocompleted values:*/
				closeAllLists();
			});
			a.appendChild(b);
		  }
		}
	});
	/*execute a function presses a key on the keyboard:*/
	inp.addEventListener("keydown", function(e) {
		var x = document.getElementById(this.id + "autocomplete-list");
		if (x) x = x.getElementsByTagName("div");
		if (e.keyCode == 40) {
		  /*If the arrow DOWN key is pressed,
		  increase the currentFocus variable:*/
		  currentFocus++;
		  /*and and make the current item more visible:*/
		  addActive(x);
		} else if (e.keyCode == 38) { //up
		  /*If the arrow UP key is pressed,
		  decrease the currentFocus variable:*/
		  currentFocus--;
		  /*and and make the current item more visible:*/
		  addActive(x);
		} else if (e.keyCode == 13) {
		  /*If the ENTER key is pressed, prevent the form from being submitted,*/
		  e.preventDefault();
		  if (currentFocus > -1) {
			/*and simulate a click on the "active" item:*/
			if (x) x[currentFocus].click();
		  }
		}
	});
	function addActive(x) {
	  /*a function to classify an item as "active":*/
	  if (!x) return false;
	  /*start by removing the "active" class on all items:*/
	  removeActive(x);
	  if (currentFocus >= x.length) currentFocus = 0;
	  if (currentFocus < 0) currentFocus = (x.length - 1);
	  /*add class "autocomplete-active":*/
	  x[currentFocus].classList.add("autocomplete-active");
	}
	function removeActive(x) {
	  /*a function to remove the "active" class from all autocomplete items:*/
	  for (var i = 0; i < x.length; i++) {
		x[i].classList.remove("autocomplete-active");
	  }
	}
	function closeAllLists(elmnt) {
	  /*close all autocomplete lists in the document,
	  except the one passed as an argument:*/
	  var x = document.getElementsByClassName("autocomplete-items");
	  for (var i = 0; i < x.length; i++) {
		if (elmnt != x[i] && elmnt != inp) {
		  x[i].parentNode.removeChild(x[i]);
		}
	  }
	}
	/*execute a function when someone clicks in the document:*/
	document.addEventListener("click", function (e) {
		closeAllLists(e.target);
	});
}
$("document").ready(function(){
	$("input[name=checkbox]").on("click",function(){
		categories = Array();
		$("input[name=checkbox]").each(function(){if(this.checked) categories.push($(this).val().toString())});
		 $("#categories").val(categories.join(",").toString());
		console.log($("#categories").val());
	});
	
});


/**
 * AMD adapter!
 * 
 * @see https://github.com/umdjs/umd
 * 
 * @author Luiz Machado <https://github.com/odahcam>
 */
 (function (root, factory) {

	if (typeof define === 'function' && define.amd) {

		// AMD. Register as an anonymous module.
		define(['exports', 'jquery'], function (exports, jquery) {
			factory((root.bootoast = exports), jquery);
		});

	} else if (typeof exports === 'object' && typeof exports.nodeName !== 'string') {

		// CommonJS
		factory(exports, require('jquery'));

	} else {

		// Browser globals
		factory((root.bootoast = {}), root.jQuery);

	}

}(this, function (exports, $) {
	// Use bootoast, bootbox in some fashion.

	'use strict';

	if (!$) {
		console.error('jQuery não encontrado, seu plugin jQuery não irá funcionar.');
		return false;
	}

	/**
	 * Store the plugin name in a variable. It helps you if later decide to change the plugin's name
	 * @var {string} pluginName
	 */
	var pluginName = 'bootoast';

	/**
	 * The plugin constructor.
	 */
	function Bootoast(options) {

		if (typeof options === 'string') {
			options = {
				message: options
			};
		}

		if (typeof options !== 'object') return;

		// define as opções interpretadas
		this.settings = $.extend({}, this.defaults, options);
		// define o conteúdo
		this.content = this.settings.content || this.settings.text || this.settings.message;
		// define o elemento de progress como nulo
		this.timeoutProgress = null;
		// define uma posição aceitável pro elemento
		this.position = this.positionFor(this.settings.position).split('-');
		// Define o .glyphicon com base no .alert-<type>
		this.settings.icon = this.settings.icon || this.icons[this.settings.type];

		var containerClass = pluginName + '-container';

		this.containerSelector = '.' + containerClass + '.' + this.position.join('.');

		// Checa se já tem container, se não cria um.
		if ($('body > ' + this.containerSelector).length === 0) {
			$('<div>', {
				class: containerClass + ' ' + this.position.join(' ')
			}).appendTo('body');
		}

		// Adiciona o .alert ao .container conforme seu posicionamento.
		this.$el = $('<div class="' + pluginName + ' alert alert-' + this.typeFor(this.settings.type) + '"><span class="glyphicon glyphicon-' + this.settings.icon + '"></span><span class="bootoast-alert-container"><span class="bootoast-alert-content">' + this.content + '</span></span></div>');

		this.init();
	}

	$.extend(Bootoast.prototype, {
		/**
		 * Default options
		 *
		 * @var {Object} defaults
		 */
		defaults: {
			/**
			 * Any HTML string.
			 * @var {string}
			 */
			message: 'Bootoast!',
			/**
			 * ['warning', 'success', 'danger', 'info']
			 * @var {string}
			 */
			type: 'info',
			/**
			 * ['top-left', 'top-center', 'top-right', 'bottom-left', 'bottom-center', 'bottom-right']
			 * @var {string}
			 */
			position: 'bottom-center',
			/**
			 * @var {string}
			 */
			icon: null,
			/**
			 * Seconds, use null to disable timeout hiding.
			 * @var {int}
			 */
			timeout: 3,
			/** 
			 * [false, 'top', 'bottom', 'background']
			 * 
			 * @var {string|bool}
			 */
			timeoutProgress: false,
			/**
			 * Animation duration in miliseconds.
			 * 
			 * @var {int}
			 */
			animationDuration: 300,
			/**
			 * @var {bool}
			 */
			dismissible: true,
		},
		/**
		 * Default icons
		 *
		 * @var {Object} icons
		 */
		icons: {
			warning: 'exclamation-sign',
			success: 'ok-sign',
			danger: 'remove-sign',
			info: 'info-sign'
		},
		/**
		 * Types
		 *
		 * @var {Object} types
		 */
		types: [
			'primary',
			'secondary',
			'info',
			'success',
			'warning',
			'danger'
		],
		/**
		 * Type Sinonymus
		 *
		 * @var {Object} typeSinonym
		 */
		typeSinonym: {
			warn: 'warning',
			error: 'danger',
		},
		/**
		 * Position Supported
		 *
		 * @var {array} positions
		 */
		positions: [
			'top-left',
			'top-center',
			'top-right',
			'bottom-left',
			'bottom-center',
			'bottom-right'
		],
		/**
		 * Position Sinonymus
		 *
		 * @var {Object} positionSinonym
		 */
		positionSinonym: {
			bottom: 'bottom-center',
			leftBottom: 'bottom-left',
			rightBottom: 'bottom-right',
			top: 'top-center',
			rightTop: 'top-right',
			leftTop: 'top-left'
		},
		/**
		 * Initializes the plugin functionality
		 */
		init: function () {

			// Define se o novo .alert deve ser inserido por primeiro ou último no container.
			this.$el[(this.position[0] === 'bottom' ? 'append' : 'prepend') + 'To'](this.containerSelector);

			var plugin = this;

			if (this.settings.dismissible === true) {
				this.$el
					.addClass('alert-dismissible')
					.prepend('<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>')
					.on('click', 'button.close', function (e) {
						e.preventDefault();
						plugin.hide();
					});
			}

			// Exibe o .alert
			this.$el.animate({
				opacity: 1,
			}, this.settings.animationDuration);

			// Se o .alert tem tempo de expiração
			if (this.settings.timeout) {

				var secondsTimeout = parseInt(this.settings.timeout * 1000);

				this.hide(secondsTimeout);
			}
		},
		/**
		 * @method hide
		 *
		 * @param {int} timeout
		 *
		 * @return {int} The setTimeout ID.
		 */
		hide: function (timeout) {
			var plugin = this;

			if (this.settings.timeoutProgress) {
				this.setTimeoutProgress(this.settings.timeoutProgress);
			}

			var timerId = setTimeout(function () {
				plugin.$el.animate({
					opacity: 0,
				}, plugin.settings.animationDuration, function () {
					plugin.$el.remove();
				});
			}, timeout || 0);

			// Pausa o timeout baseado no hover
			this.$el.hover(
				clearTimeout.bind(window, timerId),
				function () {
					timerId = plugin.hide(timeout);
				}
			);

			return timerId;
		},
		/**
		 * @param {string} progressPosition
		 * 
		 * @return {number}
		 */
		setTimeoutProgress: function (progressPosition) {

			if (this.timeoutProgress !== null) {
				this.timeoutProgress.remove();
			}

			var positionOptions = {
				top: 'prepend',
				bottom: 'append',
			};

			var $progress = $('<div>', {
				class: 'progress',
				html: $('<div>', {
					class: 'progress-bar progress-bar-striped active',
					role: 'progressbar',
					'aria-valuemin': 0,
					'aria-valuenow': 0,
					'aria-valuemax': 100,
				})
			});

			var putMethod = positionOptions[progressPosition] || 'append';
			var position = typeof positionOptions[progressPosition] === 'string' ? progressPosition : 'background';

			this.timeoutProgress = $progress.addClass('progress-' + position)[putMethod + 'To'](this.$el)

			return this.timeoutProgress;
		},
		/**
		 * @param {string} type
		 *
		 * @return {string} Gets the correct type-name for the given value or null.
		 */
		typeFor: function (type) {

			// se esta type é padrão
			if (this.types[type]) {
				return type;
			}

			if (!type) {
				return 'default';
			}

			var sinonym = this.typeSinonym[type];

			return sinonym || type;
		},
		/**
		 * @param {string} position
		 *
		 * @return {string} The correct position-name for the given value or ''.
		 */
		positionFor: function (position) {

			// se esta posição é padrão
			if (this.positions[position]) return position;

			var positionCamel = $.camelCase(position);

			// Tenta encontrar um sinônimo
			return this.positionSinonym[positionCamel] || 'bottom-center';
		},

		/**
		 *
		 * @param {HTMLElement} elem
		 * @param {int} qty
		 * 
		 * @return {int} The interval ID, so you can cancel the movement bro.
		 */
		moveProgressbar: function(elem, qty) {

			var that = this;
			var width = 100;
			
			var id = setInterval(function () {
				if (width <= 0) {
					clearInterval(id);
				} else {
					width--;
					elem.style.width = width + '%';
				}
			}, 100 / qty);

			return id;
		}
	});

	// attach properties to the exports object to define
	// the exported module properties.
	exports.toast = function (options) {
		return new Bootoast(options);
	};

	return exports;
}));