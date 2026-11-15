import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// IMPORTING LANGUAGES
import translationEN from './locales/en.json';
import translationPL from './locales/pl.json';

// Mapping imported languages
const resources = {
  en: { translation: translationEN },
  pl: { translation: translationPL }
};

const savedLanguage = localStorage.getItem('bbn-lang') || 'en';

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: savedLanguage,
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  });

// saving language change
i18n.on('languageChanged', (lng) => {
  localStorage.setItem('bbn-lang', lng);
});

export default i18n;