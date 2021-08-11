function addToCart(pk, quantity) {

    // <form action='/cart_action/'></form>
    let data = {
        'pk': pk,
        'quantity': quantity,
        'method': 'cart__plus_product'
    }


    $.post(
        "/cart_action/",
        data,
        addToCartSuccess
    );
}

function addToCartByCount(pk, quantity_element_id) {
    let quantity = document.getElementById(quantity_element_id).value;

    let data = {
        'pk': pk,
        'quantity': quantity,
        'method': 'cart__set_product'
    }

    $.post(
        "/cart_action/",
        data,
        addToCartSuccess
    );

}


function removeCart(pk) {
    let data = {
        'pk': pk,
        'method': 'cart__unset_product'
    }
    $.post(
        "/cart_action/",
        data,
        removeCartSuccess
    );
}


function minusCart(pk, quantity) {
    let data = {
        'pk': pk,
        'quantity': quantity,
        'method': 'cart__minus_product'
    }
    $.post(
        "/cart_action/",
        data,
        minusCartSuccess
    );
}

function removeCartSuccess(data) {
    // let deleted = JSON.stringify(data.deleted);
    if (data['deleted'].length > 0 && location.href.toString().includes('/cart/')) {
        console.log('here');
        RemoveElement(data['deleted'][0]);
    }
    CalculateTotal(data);
}



function minusCartSuccess(data) {
    // let deleted = JSON.stringify(data.deleted);
    if (data['deleted'].length > 0 && location.href.toString().includes('/cart/')) {
        console.log('here');
        RemoveElement(data['deleted'][0]);
    }
    changeElem(data.cart);
    CalculateTotal(data);
}

function addToCartSuccess(data) {
    // changeElem(data.cart);
    CalculateTotal(data);
}

function CalculateTotal(data) {
    console.log(data);
    let rate = document.getElementById('rate').value;
    let currency = document.getElementById('currency').value;
    let total = data.total;
    console.log(currency);
    if (currency == 'sum') {
        total = parseFloat(total) * parseFloat(rate);
    } else {
        total = total.toString() + ' $';
    }
    document.getElementById('item-count').textContent = data.total_count.toString();
    document.getElementById('total-cart').textContent = total.toString()
    if (location.href.toString().includes('/cart/')) {
        document.getElementById('total_cart_amount').textContent = total.toString();
    }
}

function ChangeCurrency(currency) {
    $.post(
        "/currency/change/",
        {
            'currency': currency
        },
        function (data) {
            location.reload();
        }
    );
}


function RemoveElement(pk) {
    document.getElementById('product' + pk.toString()).remove();
}

function changeElem(cart) {
    console.log(cart);

    let element = '<div class="cart_item">\n' +
        '                                            <div class="cart_img">\n' +
        '                                                <a href="#"><img src="{% static \'img/s-product/product.jpg\' %}" alt=""></a>\n' +
        '                                            </div>\n' +
        '                                            <div class="cart_info">\n' +
        '                                                <a href="#">JBL Flip 3 Splasroof Portable Bluetooth 2</a>\n' +
        '\n' +
        '                                                <span class="quantity">Qty: 1</span>\n' +
        '                                                <span class="price_cart">$60.00</span>\n' +
        '\n' +
        '                                            </div>\n' +
        '                                            <div class="cart_remove">\n' +
        '                                                <a href="#"><i class="ion-android-close"></i></a>\n' +
        '                                            </div>\n' +
        '                                        </div>';
    let map = new Map(Object.entries(cart));
    map.forEach(function (v, k) {
        console.log(v);
        document.getElementById('product_count' + k ).textContent = v;
        // let price = document.getElementById('product_price'+k).textContent.toString().replace('$', '');
        // document.getElementById('product_total'+k).textContent = (parseFloat(price) * parseFloat(v)).toString();
    });
}

function removeElem(pk) {
    document.getElementById('product' + pk.toString()).remove();
}




// function totalPrice () {
//      for (let i = 0; i< document.getElementsByClassName('product_total-text').length; i++){
//          let price = parseFloat($('.product-price-text').text().replace(',', '.'));
//          let input = $('.product_count' + 1);
//          let total = $('.product_total-text');
//
//     }
// }

 function calculeteTotal() {
     for (let i = 1; i < document.getElementById('shop-box').childElementCount; i++) {
         let productPrice = parseFloat(document.getElementById('product-price-' + i).textContent.replace(',','.'))
         let productCount = parseInt(document.getElementById('product_input-' + i).value)
         console.log(productPrice, productCount)
     }
 }


// $(document).ready( () => parseFloat($('.product-price-text').text().replace(',', '.')) *$('.product_quantity-text').text().replace(',', '.'))
