/** processForm: get data from form and make AJAX call to our API. */

async function processForm(evt) {
    evt.preventDefault()
    let name = $("#name").val();
    let year = $("#year").val();
    let email = $("#email").val();
    let color = $("#color").val();
    try{
    let res = await axios.post('http://127.0.0.1:5000/api/get-lucky-num',{name, year, email, color} )

    handleResponse(res)
} catch(error){
        handleResponse(error.response)}
}

/** handleResponse: deal with response from our lucky-num API. */

function handleResponse(res) {
    console.log(res)
    if (res.status == 201){    
        let lucky_num=res.data.num.num;
        let num_fact=res.data.num.fact;
        let year=res.data.year.year;
        let year_fact=res.data.year.fact;
        let result = `Your lucky number is ${lucky_num} (${num_fact}). Your birth year (${year}) fact is ${year_fact}`;
       return $("#lucky-results").text(result);

    }
    else {
        let errors = res.data.errors;
        Object.keys(errors).forEach(key => {
            $(`#${key}-err`).text(errors[key][0]);

        });
    }
    // $("#lucky-form")[0].reset();
}

$("#lucky-form").on("submit", processForm);