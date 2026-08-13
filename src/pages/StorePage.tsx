import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { supabase } from '@/lib/supabase';
import { Star, Gift, Crown, Check, ShoppingBag } from 'lucide-react';
import { useI18n } from '@/lib/i18n';

interface StoreItem {
  id: string;
  name: string;
  description: string;
  points_cost: number;
  category: string;
}

export default function StorePage() {
  const { user, profile, refreshProfile } = useAuth();
  const [items, setItems] = useState<StoreItem[]>([]);
  const [redeeming, setRedeeming] = useState<string | null>(null);
  const [redeemed, setRedeemed] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);
  const { t, isRTL } = useI18n();

  useEffect(() => {
    loadStore();
  }, [user]);

  async function loadStore() {
    setLoading(true);
    const { data: storeItems } = await supabase
      .from('store_items')
      .select('*')
      .eq('is_active', true)
      .order('points_cost');
    setItems(storeItems ?? []);

    if (user) {
      const { data: redemptions } = await supabase
        .from('store_redemptions')
        .select('store_item_id')
        .eq('user_id', user.id);
      setRedeemed(new Set((redemptions ?? []).map(r => r.store_item_id)));
    }

    setLoading(false);
  }

  async function redeemItem(item: StoreItem) {
    if (!user || !profile || profile.points_balance < item.points_cost) return;
    setRedeeming(item.id);

    await supabase.from('store_redemptions').insert({
      store_item_id: item.id,
      points_spent: item.points_cost,
    });

    await supabase.from('point_transactions').insert({
      amount: -item.points_cost,
      type: 'redeemed',
      source: 'store_redeem',
      description: `Redeemed: ${item.name}`,
    });

    await supabase
      .from('profiles')
      .update({ points_balance: profile.points_balance - item.points_cost })
      .eq('id', user.id);

    await refreshProfile();
    setRedeemed(prev => new Set([...prev, item.id]));
    setRedeeming(null);
  }

  const balance = profile?.points_balance ?? 0;

  return (
    <div className="max-w-lg mx-auto" dir={isRTL ? 'rtl' : 'ltr'}>
      {/* Header */}
      <div className="px-6 pt-12 pb-6">
        <h1 className="text-2xl font-bold text-gray-900">{t('store.title')}</h1>
        <p className="text-gray-500 text-sm">{t('store.subtitle')}</p>
      </div>

      {/* Points balance */}
      <div className="px-6 mb-6">
        <div className="bg-gradient-to-br from-amber-400 to-orange-500 rounded-2xl p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-amber-100 text-sm mb-1">{t('store.balance')}</p>
              <div className="flex items-center gap-2">
                <Star className="w-7 h-7" />
                <span className="text-4xl font-bold">{balance}</span>
              </div>
              <p className="text-amber-100 text-xs mt-1">{t('store.points_available')}</p>
            </div>
            <div className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center">
              <Gift className="w-8 h-8 text-white" />
            </div>
          </div>
        </div>
      </div>

      {/* How to earn */}
      <div className="px-6 mb-6">
        <div className="bg-emerald-50 rounded-2xl p-4 border border-emerald-100">
          <h3 className="font-semibold text-emerald-800 text-sm mb-2">{t('store.how_to_earn')}</h3>
          <div className="space-y-1.5">
            <div className="flex items-center justify-between text-sm">
              <span className="text-emerald-700">{t('store.earn.task')}</span>
              <span className="text-emerald-600 font-medium">+10-25 pts</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-emerald-700">{t('store.earn.checkin')}</span>
              <span className="text-emerald-600 font-medium">+15 pts</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-emerald-700">{t('store.earn.all_tasks')}</span>
              <span className="text-emerald-600 font-medium">+50 pts</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-emerald-700">{t('store.earn.streak')}</span>
              <span className="text-emerald-600 font-medium">+100 pts</span>
            </div>
          </div>
        </div>
      </div>

      {/* Store items */}
      <div className="px-6 pb-6">
        <h3 className="font-semibold text-gray-900 mb-3">{t('store.available')}</h3>
        {loading ? (
          <div className="flex justify-center py-12">
            <div className="w-6 h-6 border-2 border-emerald-200 border-t-emerald-600 rounded-full animate-spin" />
          </div>
        ) : items.length === 0 ? (
          <div className="bg-white rounded-2xl border border-gray-100 p-8 text-center">
            <ShoppingBag className="w-8 h-8 text-gray-300 mx-auto mb-2" />
            <p className="text-gray-400 text-sm">{t('store.no_items')}</p>
          </div>
        ) : (
          <div className="space-y-4">
            {items.map(item => {
              const canAfford = balance >= item.points_cost;
              const alreadyRedeemed = redeemed.has(item.id);
              const isRedeeming = redeeming === item.id;

              return (
                <div key={item.id} className="bg-white rounded-2xl border border-gray-100 overflow-hidden">
                  <div className="bg-gradient-to-r from-emerald-500 to-teal-600 p-4 flex items-center gap-3">
                    <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center">
                      <Crown className="w-6 h-6 text-white" />
                    </div>
                    <div className="text-white flex-1">
                      <p className="font-bold">{item.name}</p>
                      <div className="flex items-center gap-1 mt-0.5">
                        <Star className="w-3.5 h-3.5 text-amber-300" />
                        <span className="text-sm text-emerald-100">{item.points_cost.toLocaleString()} points</span>
                      </div>
                    </div>
                  </div>
                  <div className="p-4">
                    <p className="text-sm text-gray-600 mb-4">{item.description}</p>
                    {alreadyRedeemed ? (
                      <div className="flex items-center gap-2 text-emerald-600 bg-emerald-50 px-4 py-2.5 rounded-xl">
                        <Check className="w-4 h-4" />
                        <span className="text-sm font-medium">{t('store.redeemed')}</span>
                      </div>
                    ) : (
                      <button
                        onClick={() => redeemItem(item)}
                        disabled={!canAfford || isRedeeming}
                        className={`w-full py-3 rounded-xl font-medium text-sm transition-all flex items-center justify-center gap-2 ${
                          canAfford
                            ? 'bg-emerald-600 hover:bg-emerald-700 text-white shadow-lg shadow-emerald-600/20'
                            : 'bg-gray-100 text-gray-400 cursor-not-allowed'
                        }`}
                      >
                        {isRedeeming ? (
                          <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        ) : canAfford ? (
                          <>{t('store.redeem')}<Gift className="w-4 h-4" /></>
                        ) : (
                          t('store.need_more', { amount: (item.points_cost - balance).toLocaleString() })
                        )}
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
