let updateBtns = document.getElementsByClassName('update-cart')
const cartNum = document.getElementById('cartNum')
const addToCart = document.getElementById('add-to-cart')
let dataVar;


const getBtn =()=>{
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
}

getBtn()




function updateUserOrder(productId, action){
let cartNumber = document.getElementById('cart-number-container')
let order = document.getElementById('order')
let total= document.getElementById('total')


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
          dataVar = data.data
          console.log("dataVar",dataVar)
          cartNumber.innerHTML = data.cartItems
          order.innerHTML = data.cartItems
          total.innerHTML = data.get_cart_total
          getData ()


                })
}

let postbox = document.getElementById('post-box')
const getData =()=>{
postbox.innerHTML=""

 console.log("last",dataVar)
 dataVar.forEach(el=>{

                    postbox.innerHTML +=`
                          <hr>
                        <div class="order-container2" >
                        <div><img class="order-img" src="${el.image}"></div>
                        <div > ${el.product}</div>
                        <div class="order-price">${el.price}</div>
                        <div class="quantity">
                            <span class="quatity-number">${el.quantity}</span>
                            <div class="quatity-img">

                                     <div>
                                              <button href="#" class="update-cart" data-form-id='${el.id}' data-product="${el.id}" data-action="add">
                                              <img class="quantity-arrow-down " src="/static/images/arrow-up.png"></button>
                                     </div>



                                     <div>
                                             <button href="#" class="update-cart"  data-form-id='${el.id}' data-product="${el.id}" data-action="remove">
                                             <img class="quantity-arrow-down " src="/static/images/arrow-down.png"></button>
                                     </div>



                            </div>
                        </div>
                        <div class="total">${el.get_total}</div>



                    </div>


          `
      }




);
getBtn()



}




