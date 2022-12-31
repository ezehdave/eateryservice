let updateBtns = document.getElementsByClassName('update-cart')
const cartNum = document.getElementById('cartNum')
const addToCart = document.getElementById('add-to-cart')


for(let i = 0; i< updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
    let productId = this.dataset.product
    let action = this.dataset.action
    console.log('productId:', productId, 'action:',action)

    console.log('USER:', user)
    if (user ==='AnonymousUser'){
         console.log('not logged in')
    }else{
        updateUserOrder(productId, action)

    }
    })

}

let cartNumber = document.getElementById('cart-number-container')



function updateUserOrder(productId, action){

     console.log('User is logged in, sending data..')
     let url = '/update_item/'
     fetch(url, {
         method: 'POST',
         headers:{
              'content-Type':'application/json',
              'X-CSRFToken': csrftoken
         },
         body:JSON.stringify({'productId': productId, 'action': action})
      })
        .then((response) => response.json())
        .then((data) => {
          console.log('success:', data);

          console.log('success:', data.cartItems);


          cartNumber.innerHTML = data.cartItems


        })

}




