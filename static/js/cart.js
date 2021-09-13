var updateBtns = document.getElementsByClassName("장바구니업데이트")
for(var i=0; i<updateBtns.length; i++){
  updateBtns[i].addEventListener("click", function(){
    var productID = this.dataset.product //data-product={{product.id}}
    var action = this.dataset.action //data-action="add" 

    if(user == 'AnonymousUser'){//var user = "{{request.user}}" (base.html에서가져옴)
      //alert("로그인 후 이용바랍니다.")
      //->로그인 안해도 쿠키이용해 장바구니 이용하게끔 변경
      addCookieItem(productID, action)
    }
    else{
      updateUserOrder(productID, action)
    }
  })
}

function addCookieItem(productID, action) {
  if (action == 'add'){
    if (cart[productID] == undefined){
      cart[productID] = {'quantity':1}
    }
    else {
      cart[productID]['quantity'] += 1
    }
  }

  if (action == 'sub'){
    cart[productID]['quantity'] -= 1
    if (cart[productID]['quantity'] <= 0){
      delete cart[productID];
    }        
  }
  
  document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
  location.reload()
}


function updateUserOrder(productID, action){
  var url ='/update_item/'
  fetch(url, { //패치 이용 (정보 전송)
    method: 'POST', //전송방식(업데이트)
    headers: { //헤더 포함내용
      'Content-Type':'application/json',
      'X-CSRFToken': csrftoken //패치 해킹방지 (csrf토큰, base에서 가져옴)
    },
    body: JSON.stringify({'productID':productID, 'action':action}) //바디 내용
  })
  .then((response)=>{ //응답받으면 (데이터를 받음)
    return response.json() 
  })
  .then((data)=>{ //받은 데이터 활용
    console.log('data:', data)
    location.reload()//자바스크립이 자동으로 새로고침(즉, 장바구니담기버튼누를때마다)
  })
}