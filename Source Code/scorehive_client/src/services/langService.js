import translations from "@/services/translations.json"
const defaultLanguage = 'en';
export function getTranslation(language) {
  return translations[language] || translations[defaultLanguage] || {};
}
export default {
  translate(key, language) {
    const translation = getTranslation(language);
    return translation[key] || '';
  }
}