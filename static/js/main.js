$(document).ready(function(){
	$('body').addClass('a');

	rebind();

});

function rebind(){
	$('#engineering').click(function(){
		$('body').toggleClass('engineering');
	});

	$('#aviation').click(function(){
		$('body').toggleClass('aviation');
	});

	$('body.aviation h1').click(function(){
		$('body').removeClass('aviation');
		$('body').addClass('b');
		rebind();
	});

	$('body.b h1').click(function(){
		$('body').removeClass('b');
		$('body').addClass('engineering');
		rebind();
	});
}
