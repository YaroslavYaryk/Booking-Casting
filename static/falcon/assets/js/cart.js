var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
    updateUserCart(productId, action)
	})
}

function updateUserCart(productId, action){

		var url = '/update_cart/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
			},
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}
