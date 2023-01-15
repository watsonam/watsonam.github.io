<p>
  hello world
</p>
<!-- <script>
  import { onMount } from 'svelte';
  import markdown from 'svelte-markdown';

  let articles = [
    { year: 2022, text: './articles/2022-article-1.md' },
    { year: 2021, text: './articles/2021-article-2.md' },
    { year: 2020, text: './articles/2020-article-3.md' },
    { year: 2019, text: './articles/2019-article-4.md' },
    { year: 2018, text: './articles/2018-article-5.md' }
  ];

  onMount(async () => {
    // Fetch the markdown text for each article
    articles = await Promise.all(articles.map(async (article) => {
      const response = await fetch(article.text);
      article.text = await response.text();
      return article;
    }));
  });
</script>

<style>
  /* Styles for the blog page */
  .articles {
    display: flex;
    flex-wrap: wrap;
  }

  .article {
    width: 100%;
    margin-bottom: 2rem;
    padding: 1rem;
    box-sizing: border-box;
  }

  .year {
    font-size: 1.5rem;
    font-weight: bold;
    margin-right: 1rem;
  }
</style>

<div class="articles">
  {#each articles as article}
    <div class="article">
      <div class="year">{article.year}</div>
      <svelte-markdown>{article.text}</svelte-markdown>
    </div>
  {/each}
</div> -->
