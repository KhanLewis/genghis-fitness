$(document).ready(function() {
  $(".add-to-cart-button").click(function(event) {
    event.preventDefault();
    var form = $(this).closest(".add-to-cart-form");
    var productId = form.find("input[name='product_id']").val();

    $.ajax({
      type: "POST",
      url: "/cart/add/" + productId + "/",
      data: form.serialize(),
      success: function(response) {
        // Update the cart count in the dropdown
        var cartCount = parseInt($("#cart-count").text());
        $("#cart-count").text(cartCount + 1);

        // Show the success message
        $(".alert").removeClass("d-none");

        // Auto-dismiss the success message after 3 seconds
        setTimeout(function() {
          $(".alert").alert("close");
        }, 3000);
      },
      error: function(xhr, textStatus, errorThrown) {
        console.log(xhr.responseText);
      }
    });
  });
});