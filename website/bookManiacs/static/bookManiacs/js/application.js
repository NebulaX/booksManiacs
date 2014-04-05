$(document).ready(function (){
	
	$("#headerContent a").tooltip();

	$("#signup").submit(function (event)
	{
		var a=$("#name");
		if(!(a.val().match(/^[a-zA-Z ]+$/)))
		{
			alert("Please enter a valid name");
			a.focus();
			return false;
		}
		var a=$("#phone");
		if(!(a.val().match(/^[789]\d{9}$/)))
		{
			alert("Please enter a valid phone number");
			a.focus();
			return false;
		}
		var a=$("#password");
		var b=$("#confirm_password");
		if( a.val()=="" ){
			alert("Please enter a valid password");
			a.focus();
			return false;
		}
		if(!a.val()==b.val()){
			alert("Password Mismatch !!");
			a.focus();
			return false;
		}
	});

	$("#about-control").click(function(){
		var slide_flag = $("#about-control i");
		if (slide_flag.hasClass("fa-angle-double-up")) {
			aboutSlideUp();
			slide_flag.removeClass("fa-angle-double-up").addClass("fa-angle-double-down");
		}
		else {
			aboutSlideDown();
			slide_flag.removeClass("fa-angle-double-down").addClass("fa-angle-double-up");
		}
	});
});

function aboutSlideDown(){
	$("#about").animate({bottom: "-236px"}, 500);
}

function aboutSlideUp() {
	$("#about").animate({bottom: "0px"}, 500);
}

function coverUp(){
	$("#cover").fadeOut();
}