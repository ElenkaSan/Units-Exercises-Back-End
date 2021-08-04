const urlPage = 'http://localhost:5000/api';

async function SeeCupcakesOnPage() {
	const response = await axios.get(`${urlPage}/cupcakes`);
	cupcakes = response.data.cupcakes;

	for (let cupcake of cupcakes) {
		$(showCupcakes(cupcake));
	}
}

function showCupcakes(cupcake) {
	let addCupcake = `
  
        <div cupcake_id = ${cupcake.id}>
            <img class= "img" src="${cupcake.image}" alt="No Image">
            <h4>${cupcake.flavor} Cupcake</h4>
            <h5>Rating: ${cupcake.rating} / Size: ${cupcake.size}</h5>
            <button class="btn-delete">Remove</button>
        </div>`;

	$('#see-cupcakes').append(addCupcake);
}

$('#make-cupcake').on('submit', async function(evt) {
	evt.preventDefault();

	let flavor = $('#flavor').val();
	let rating = $('#rating').val();
	let size = $('#size').val();
	let image = $('#image').val();

	const response = await axios.post(`${urlPage}/cupcakes`, {
		flavor,
		rating,
		size,
		image
	});

	console.log(response.data);

	$(showCupcakes(response.data.cupcake));
  $("#make-cupcake").trigger('reset');
});

$('#see-cupcakes').on('click', '.btn-delete', async function(evt) {
	evt.preventDefault();

	let $cupcake = $(evt.target).closest('div');
	let cupcakeId = $cupcake.attr('cupcake_id');

	await axios.delete(`${urlPage}/cupcakes/${cupcakeId}`);

	$cupcake.remove();
});

$(showCupcakes);

