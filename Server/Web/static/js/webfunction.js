// front에서 기동하는 모든 js코드
//import Axios from 'axios';

//const axios =require('axios')


function get_worst_10() {
	axios("http://thanos-ip.com/worst-ip/10",{
	method:"get",
	}).then((response) => {
		console.log(response);
		for (let i=0; i<Object.keys(response.data).length; i++){
			console.log('worst{0}'.format(i+1));
			const rank = document.querySelector('.worst{0}'.format(i+1));
			rank.innerText=response.data[(i+1).toString()];
		}
	}).catch((error) => {
		console.log(error);
	})
}
get_worst_10();


function get_popular_10() {
	axios("http://thanos-ip.com/search_rank/10",{
	method:"get",
	}).then((response) => {
		console.log(response.data)
	}).catch((error) => {
		console.log(error);
	})
}

get_popular_10();
