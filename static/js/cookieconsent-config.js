/**
 * https://playground.cookieconsent.orestbida.com/
 * All config. options available here:
 * https://cookieconsent.orestbida.com/reference/configuration-reference.html
 */
CookieConsent.run({

    autoShow: true,
    disablePageInteraction: true,
    hideFromBots: false,

    cookie: {
        name: 'cc_cookie',
    },

    guiOptions: {
        consentModal: {
            layout: 'box',
            position: 'bottom center',
            equalWeightButtons: true,
            flipButtons: false
        },
        preferencesModal: {
            layout: 'box',
            equalWeightButtons: false,
            flipButtons: true
        }
    },

    onFirstConsent: ({cookie}) => {
    },

    onConsent: ({cookie}) => {
    },

    onChange: ({changedCategories, changedServices}) => {
    },

    onModalReady: ({modalName}) => {
    },

    onModalShow: ({modalName}) => {
    },

    onModalHide: ({modalName}) => {
    },

    categories: {
        necessary: {
            enabled: true,  // this category is enabled by default
            readOnly: true  // this category cannot be disabled
        },
        analytics: {
            autoClear: {
                cookies: [
                    {
                        name: /^_ga/,   // regex: match all cookies starting with '_ga'
                    },
                    {
                        name: '_our_services',   // string: exact cookie name
                    }
                ]
            },

            services: {
                our_services: {
                    label: 'Product Suggestions',
                    onAccept: () => {
                        
                    },
                    onReject: () => {
                        
                    }
                },
            }
        },
        ads: {}
    },

    language: {
        default: 'en',
        translations: {
            en: {
                consentModal: {
                    title: 'We use cookies',
                    description: 'We use cookies and similar tracking technologies to enhance your browsing experience, analyze our website traffic, and personalize content and advertisements. By clicking "Accept All Cookies," you agree to the storing of cookies on your device to improve site navigation, analyze site usage, and assist in our marketing efforts. You can manage your cookie preferences by clicking "Manage Cookies" in our website footer and amend your consent at any time.',
                    acceptAllBtn: 'Accept all',
                    acceptNecessaryBtn: 'Reject all',
                    showPreferencesBtn: 'Manage Individual preferences',
                    footer: `
                        <a href="https://8000-bowlesy666-ameliamaecos-1vyy92zunob.ws-eu108.gitpod.io/privacy_policy/" target="_blank">Privacy Policy</a>
                        <a href="https://amelia-mae-cosmetics-5de0b8a03e08.herokuapp.com/privacy_policy/" target="_blank">Privacy Policy</a>
                    `,
                },
                preferencesModal: {
                    title: 'Manage cookie preferences',
                    acceptAllBtn: 'Accept all',
                    acceptNecessaryBtn: 'Reject all',
                    savePreferencesBtn: 'Accept current selection',
                    closeIconLabel: 'Close modal',
                    serviceCounterLabel: 'Service|Services',
                    sections: [
                        {
                            title: 'Your Privacy Choices',
                            description: `Customize your cookie settings to suit your preferences. Select which types of cookies you consent to below. You can change your preferences at any time by revisiting this page, clicking on the manage cookies button in the website footer.`,
                        },
                        {
                            title: 'Strictly Necessary',
                            description: 'These cookies are essential for the proper functioning of the website and cannot be disabled.',

                            //this field will generate a toggle linked to the 'necessary' category
                            linkedCategory: 'necessary'
                        },
                        {
                            title: 'Performance and Analytics',
                            description: 'These cookies collect information about how you use our website. All of the data is anonymized and cannot be used to identify you.',
                            linkedCategory: 'analytics',
                            cookieTable: {
                                caption: 'Cookie table',
                                headers: {
                                    name: 'Cookie',
                                    domain: 'Domain',
                                    desc: 'Description'
                                },
                                body: [
                                    {
                                        name: 'Product suggestions',
                                        domain: location.hostname,
                                        desc: 'Tailored product suggestions for you',
                                    }
                                ]
                            }
                        },
                        {
                            title: 'More information',
                            description: 'For any queries in relation to our policy on cookies and your choices, please view our <a href="https://amelia-mae-cosmetics-5de0b8a03e08.herokuapp.com/cookie_policy/">Cookie Policy.</a>'
                        }
                    ]
                }
            }
        }
    }
});