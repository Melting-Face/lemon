import { load } from 'cheerio';
import request from 'modules/request';

const baseUrl = 'https://www.hani.co.kr';

(async () => {
  const response = await request('https://www.hani.co.kr/arti/economy/it/gallery1.html');
  const $ = load(response);
  const listUrls: any = [];
  $('.article-area').each((_i, div) => {
    const pathUrl = $(div).find('.article-title a').attr('href');
    listUrls.push(`${baseUrl}${pathUrl}`);
  });

  const articles = [];

  for (const listUrl of listUrls) {
    const response = await request(listUrl);
    const $ = load(response);
    const title = $('h4 .title').text().trim();
    const subTitle = $('.subtitle').text().trim();
    $('.image-area').remove();
    const article = $('.article-text .text').text().trim();
    articles.push({
      title,
      subTitle,
      article,
    })
  }

  console.info(articles)

  await request({
    url: 'http://127.0.0.1:9999/insert/articles',
    method: 'POST',
    body: articles,
  })
})();
