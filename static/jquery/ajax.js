$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});

//Ajax recherche par genre
$(function(){ // Attendre que le document soit totalement chargé, équivaut à $(document).ready(function(){

	$('#search').keyup(function() { // le # fait référence à l'id qui doit être unique. Utilise lorsque le l'on veut qu'un unique élément
									// .search pour une class (class = search)
									// nom balise html, par exemple p, div,...

		$.ajax({
			type: "GET",
			url: "/blog_livreSF/ajax/search/",
			data: {
				'search_text' : $('#search').val()
			},

			dataType: 'html',
			success: function(data, textStatus, jqXHR){
				$('#search-results').html(data);
			}
			
		});

	});

});

// Ajax recherche par tag
$(function(){
	$('.liste_tags').click(function(){
		var this_ = $(this);
		var id_tag = this_.attr('id_tag');
		console.log(id_tag)
		$.ajax({
			type: "GET",
			url: "/nouvelle/ajax/nuage_tag/",
			data: {
				'id_tag': id_tag
			},

			success: function(data){
				$('#search-tags').html(data);	
			}
		})
	})
});

 // Attendre que le document soit totalement chargé, équivaut à $(document).ready(function(){

function updateText(btn, newCount, verb){ // fonction qui va servir d'affichage
	btn.text(newCount + " " + verb)
}
$(function(){

	$('.like-btn').click(function(e) { // le # fait référence à l'id qui doit être unique. Utilise lorsque le l'on veut qu'un unique élément
										// .search pour une class (class = search)
										// nom balise html, par exemple p, div,...
		e.preventDefault()
		var this_ = $(this); // On prend le bouton 
		var PhotoURL = this_.attr("position-photo");
		var NamePhoto = this_.attr("name-photo");
		var likeURL = this_.attr("data-href"); // Récolte le contenu des attributs du bouton, ici l'url 
		console.log(likeURL); // Affichage console pour vori ce que l'on fait
		$.ajax({
			type: "GET",
			url: likeURL,
			data: {}, 

			success: function(data){ // data provient de ce que renvoie likeURL
				if (data.liked){ // voir contenu de data 
					PhotoURL = PhotoURL+'image_site/like_button.png'
					updateText(this_, data.count, '')  // Ajout d'une fonction pour affichage
					$('#'+NamePhoto).attr('src', PhotoURL) // change l'attribut, ici le lieu de stockage de l'image
					$('#'+NamePhoto).css('display', 'inline') // change propriété css, ici display
				} else{
					updateText(this_, data.count, '') 
					PhotoURL = PhotoURL+'image_site/no_like_button.png'
					$('#'+NamePhoto).attr('src', PhotoURL)
					$('#'+NamePhoto).css('display', 'inline')
				}
			}, error: function(error){
				console.log(error)
				console.log("error")
			}
			
		});

	});

});

// Requete ajax pour ajouter un genre litteraire
$(function(){
	$('#button_sub').click(function(){
		var this_ = $(this);
		var new_genre = $('#new_genre').val();
		$.ajax({
			type: "POST",
			url: "/blog_livreSF/ajax/add_genre/",
			data: {
				'new_genre' : new_genre
			},

			success: function(data){
				$('#all_genre').html(data);
				$('#hide_new_genre').hide();
				$('#success_message').css('display', 'inline');
			}
		});
	});
});

// Requete Ajax pour ajouter un tag à une nouvelle
$(function(){
	$('#button_sub_tag').click(function(){
		var this_ = $(this);
		var new_tag = $('#new_tag').val();
		$.ajax({
			type: "POST",
			url: "/nouvelle/ajax/add_tag/",
			data: {
				'new_tag' : new_tag
			},

			success: function(data){
				$('#all_tag').html(data); //Affiche la donnée
				$('#hide_new_tag').hide(); //On cache le précédant form sur le tag, cf form_help.html
				$('#success_message').css('display', 'inline');
			}
		});
	});
});

// Faire apparaitre ou non les commentaires de l'auteur 
$(function(){
	$('#commentaire_auteur').click(function(){
		if ($('#commentaire_auteur_show').css('display') == 'none'){
			if ($('#confirmation_commentaire_auteur').css('display') == 'none')
			{
				$('#confirmation_commentaire_auteur').show()
				$('#confirmation_commentaire_auteur_ok').show()
			}
			else{
				$('#confirmation_commentaire_auteur').hide()
				$('#confirmation_commentaire_auteur_ok').hide()
			}
			
		}
		else{
			$('#commentaire_auteur_show').hide()
		}
	})
	$('#confirmation_commentaire_auteur_ok').click(function(){
		$('#commentaire_auteur_show').show()
		$('#confirmation_commentaire_auteur').hide()
		$('#confirmation_commentaire_auteur_ok').hide()
	})
})

// En cas de suppression d'un message ou d'un blog :
$(function(){
	$('#tenta1').click(function(){
		$('#tenta1').hide();
		$('#tenta1_message').css("display", "inline");
		$('#tenta2').show();
	});
	$('#tenta2').click(function(){
		$('#tenta2').hide();
		$('#tenta2_message').css("display", "inline");
		$('#tenta3').show();
	});
	$('#tenta3').click(function(){
		$('#tenta3').hide();
		$('#tenta3_message').css("display", "inline");
		$('#tenta4').show();
	});

	$('#tenta4').click(function(){
		$('#tenta4').hide();
		$('#tenta4_message').css("display", "inline");
		$('#tenta5').show();
	});

	$('#tenta5').click(function(){
		var this_ = $(this); // On prend le bouton 
		var isLast = this_.attr("isLast");
		if (isLast == 'True'){
			$('#tenta5').hide();
			$('#tenta5_message').css("display", "inline");
			$('#final_tenta').show();
			$('#cancel_button').hide();
		} else{
			$('#tenta5').hide();
			$('#tenta5_message').css("display", "inline");
			$('#tenta6').show();
		}
	});

	$('#tenta6').click(function(){
		$('#tenta6').hide();
		$('#tenta6_message').css("display", "inline");
		$('#tenta7').show();
	});
	$('#tenta7').click(function(){
		$('#tenta7').hide();
		$('#tenta7_message').css("display", "inline");
		$('#final_tenta').show();
		$('#cancel_button').hide();
	});
});

// Pour savoir à quel onglet on se trouve :
$(document).ready(function(){

	var pathname = window.location.pathname ;
	// var pathname = pathname.slice(1).slice(0,-1)
	// var selector = "a[href*='" + pathname +"']"
	// var selector_hover = selector + ":hover"
	if( pathname.indexOf('nouvelle') > -1){
		$('#entourer_nouvelle').css('display', 'inline')
	}
	if( pathname.indexOf('film') > -1){
		$('#entourer_film').css('display', 'inline')
	}
	if( pathname.indexOf('profile') > -1){
		$('#entourer_profile').css('display', 'inline')
	}
	if( pathname.indexOf('blog_livreSF') > -1){
		$('#entourer_blog_livre_SF').css('display', 'inline')
	}
	if( pathname.indexOf('forum') > -1){
		$('#entourer_forum').css('display', 'inline')
	}
	console.log(pathname)
	if( pathname.indexOf('connexion') > -1){
		console.log("oui")
		$('#entourer_connexion').css('display', 'inline')
		// $('#navbar .navbar-right a[href*="connexion"]:hover').css('color','#000')
	}

});

$(function(){
	$.ajax({
		type: "GET",
		url: "/connexion/ajax/message_non_lu/",

		success: function(data, textStatus, jqXHR){
			$('#nombre_message_non_lu').html(data);
		}
	})
})

// Partie commentaire pour voir plus ou moins :
$(document).ready(function(){
	$('.comment_button').click(function() {
		var this_ = $(this);
		var id_comment = this_.attr("id_comment");
		var href_url = this_.attr("href");
		var message_id_comment = "#message_"+id_comment
		console.log(message_id_comment)
		$.ajax({
			type: "POST",
			url: href_url,
			data: {
				'id_comment': id_comment,
			},

			success: function(data){
				$(message_id_comment).html(data)
			}
		})
	})

	$("div[id='button_more_comment'").click(function(){
		var this_ = $(this);
		var id_comment = this_.attr("id_comment")
		var id_long = "#show_long_comment_" + id_comment
		var id_short = "#show_short_comment_" + id_comment
		console.log(id_comment, id_long, id_short)
		$(id_long).css("display", "inline")
		$(id_short).css("display", "none")

	})

	$("div[id='button_less_comment'").click(function(){
		var this_ = $(this);
		var id_comment = this_.attr("id_comment")
		var id_long = "#show_long_comment_" + id_comment
		var id_short = "#show_short_comment_" + id_comment
		$(id_long).css("display", "none")
		$(id_short).css("display", "inline")

	})
})



				// 'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()

// $(document).ready(function() {
// 	$("#test").load(function(){

// 	});
// });


// $(document).ready(function() {
// 	$(window).scroll(function () {
// 	//if you hard code, then use console
// 	//.log to determine when you want the 
// 	//nav bar to stick.  
// 		console.log($(window).scrollTop())
// 		if ($(window).scrollTop() > 280) {
// 			$('.navbar').addClass('sticky');
// 		}
// 		if ($(window).scrollTop() < 281) {
// 			$('.navbar').removeClass('sticky');
// 		}
// 	});
// });

// $(document).ready(function() {
// 	window.onscroll = function() {myFunction()};

// 	var test = document.getElementById("#test");
// 	var sticky = test.offsetTop;

// 	function myFunction() {
// 		if (window.pageYOffset >= sticky) {
// 		test.classList.add("sticky")
// 		} else {
// 		test.classList.remove("sticky");
// 		}
// 	}
// });
