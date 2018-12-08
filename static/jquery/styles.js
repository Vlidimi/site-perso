$(window).width()

$(document).ready(function() {
	$(".btn-group .btn").click(function () {
	    $(".btn-group .btn ").removeClass("btn-primary").addClass("btn-default");
	    // $(".tab").addClass("active"); // instead of this do the below 
	    $(this).removeClass("btn-default").addClass("btn-primary");   
	});
});

$(document).on('click','.nav-link.active', function(){
  var href = $(this).attr('href').substring(1);
  $(this).removeClass('active');
  $('.tab-pane[id="'+ href +'"]').removeClass('active');
})