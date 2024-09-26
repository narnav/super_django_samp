let products = []
        const SERVER = "http://127.0.0.1:8000/"
        let cart = []
        let total = 0
        let userName = ""

        const register=async()=>{
            await axios.post(SERVER + "register", { username: username.value, password: password.value,email:"aa@aaa.com" }).then(res => console.log(res.data))
        }


        const getUsernameFromToken = (token) => {
            // Split the token to get the payload
            const payload = token.split('.')[1];

            // Decode the payload
            const decodedPayload = JSON.parse(atob(payload));

            // Return the username
            return decodedPayload.username;
        }


        const login = async () => {
            await axios.post(SERVER + "login", { username: username.value, password: password.value }).then(res => localStorage.setItem("token", res.data.access))
            userName = getUsernameFromToken(localStorage.getItem('token'))
            greet.innerHTML = "<h1>Welcome: " + userName + "<button onClick='checkout()'>Checkout</button>"
        }
        const checkout = () => {
            if (cart.length == 0) {
                console.log("your cart empty");
            }
            else //checkout - not empty cart
            {
                // console.log(JSON.stringify(cart) );
                axios.post(SERVER + "orders/", cart, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`, // Common way to send token
                    }
                })
            }
        }

        const loadData = async () => {
            products = await axios(SERVER + "products/")
            products = products.data
            build_display()
        }
        loadData()

        const build_display = () => {
            display.innerHTML = products.map((prod, ind) => `<div>
                Description :${prod.desc}
                price:${prod.price}
                <button onClick='buy(${JSON.stringify(prod)},1)'> Buy</button>
                </div>` ).join("")
        }

        const buy = (super_prod, amount) => {
            let temp_prod = cart.filter(prod => prod.id == super_prod.id)[0]

            if (temp_prod == undefined) {
                temp_prod = super_prod
                temp_prod.amount = amount
                cart.push(temp_prod)
            }
            else {
                if (temp_prod.amount + amount == 0) {
                    cart = cart.filter(prod => prod.id != super_prod.id)
                }
                temp_prod.amount += amount
            }
            build_cart_display()
        }

        const build_cart_display = () => {
            cart_display.innerHTML = cart.map((prod, ind) => `<div>
                desc :${prod.desc}
                price:${prod.price}
                amount:${prod.amount}
                <button onClick='buy(${JSON.stringify(prod)},1)'> Add</button>
                <button onClick='buy(${JSON.stringify(prod)},-1)'> remove</button>
                </div>` ).join("")

            total = 0
            cart.forEach(prod => total += prod.price * prod.amount)
            total_display.innerHTML = " Only:" + total
        }