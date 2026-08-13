import AsyncStorage from '@react-native-async-storage/async-storage';
import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';

const useSecure = Platform.OS !== 'web';

export async function storeGet(key: string): Promise<string | null> {
  try {
    if (useSecure) return await SecureStore.getItemAsync(key);
    return await AsyncStorage.getItem(key);
  } catch {
    return null;
  }
}

export async function storeSet(key: string, value: string): Promise<void> {
  try {
    if (useSecure) await SecureStore.setItemAsync(key, value);
    else await AsyncStorage.setItem(key, value);
  } catch {
    /* storage unavailable — session stays in memory */
  }
}

export async function storeDel(key: string): Promise<void> {
  try {
    if (useSecure) await SecureStore.deleteItemAsync(key);
    else await AsyncStorage.removeItem(key);
  } catch {
    /* ignore */
  }
}
