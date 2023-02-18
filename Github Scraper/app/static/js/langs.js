const header = { method:"GET",
headers : {Authorization : 'token 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'
} }

let url = "https://api.github.com/users/pyguru123/repos";
fetch(url, header)
.then(response => response.json())
.then(repos => {
    const requests = repos.map(repo => !repo['fork'] && fetch(repo['languages_url'], header));

    Promise.all(requests)
    .then(responses => Promise.all(responses.map(response => response.json())))
    .then(output => calculate_top_languages(output));

    function calculate_top_languages(output) {
        const all_languages = {}
        var total = 0;

        for (var index=0; index<output.length; index++) {
            languages = output[index];

            if (languages) {
                for (const language in languages) {
                    if (language in all_languages) {
                        all_languages[language] += languages[language];
                    }
                    else {
                        all_languages[language] = languages[language]
                    }
            
                    total += languages[language];
                }
            }
        }

        var sorted_langs = Object.entries(all_languages);
        sorted_langs.sort(function(a, b) {
            return a[1] - b[1];
        }).reverse();

        for (lang of sorted_langs) {
            perc = ((lang[1]/total) * 100).toFixed(2)
            console.log(lang[0] + " : " + perc);
        }
    }
});