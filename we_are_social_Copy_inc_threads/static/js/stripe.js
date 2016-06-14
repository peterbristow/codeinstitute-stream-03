/**
 * Created by Peter on 20/05/2016.
 * Define what happens when the register-for is submitted.
 */
$(function () {
    $("#register-form").submit(function () {
        var form = this;

        // collect details - will be added to the Stripe.createToken() function
        var card = {
            number: $("#id_credit_card_number").val(),
            expMonth: $("#id_expiry_month").val(),
            expYear: $("#id_expiry_year").val(),
            cvc: $("#id_cvv").val()
        };

        // disable the validate_card_btn so it isn’t triggered again while
        // waiting for Stripe to assign us a token/id.
        $("#validate_card_btn").attr("disabled", true);

        // Call to Stripe using the createToken function and pass in the card details.
        Stripe.createToken(card, function (status, response) {
            // create handler function to control what happens when the request succeeds/fails.
            if (status === 200) { // If successful
                console.log(status, response);
                // Hide errors if any previously existed.
                $("#credit-card-errors").hide();
                // Add stripe token/id into the existing stripe_id field ready
                // to be posted back to the server.
                $("#id_stripe_id").val(response.id);
                // Post form back to the server to complete registration process.
                form.submit();

            } else {
                $("#stripe-error-message").text(response.error.message);
                $("#credit-card-errors").show();
                $("#validate_card_btn").attr("disabled", false);
            }
        });
        return false;
    });
});
