const url = `${BASE_URL}/dashboard/cctv/api/datamaster`

$(document).ready( function () {
	$('#myTable').DataTable({
		serverSide: true,
		searching: true,
		processing: true,
		columnDefs: [{
			defaultContent: '-',
			targets: '_all'
		}],
		ajax: {
			type: 'GET',
			url: url,
		},
		lengthMenu: [
			[5,10,20],
			[5,10,20],
		],
		length: 5,
		columns: [
			{
				data: "source"
			},
			{
				data: "cctv_code"
			},
			{
				data: "created_at"
			},
		],
		
	});
});